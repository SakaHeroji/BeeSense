#!/usr/bin/env python3
"""YouTube source adapter; shared tables live exclusively in social_common.py.

Uses yt-dlp's unofficial web extraction, without a YouTube Data API key.
Does not download video/audio, use cookies, solve challenges, or bypass login.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import importlib.metadata
import json
import multiprocessing as mp
import os
from pathlib import Path
import re
import signal
import sys
import time
import uuid
from urllib.parse import parse_qs, quote, urlencode, urlsplit

if __package__:
    from .social_common import (BundleSink, ContentInput, Dataset, KeywordMatcher, RecordFactory, SourceAdapter,
        add_readme, now_iso, schema_fingerprint, verify_descriptor)
else:
    from social_common import (BundleSink, ContentInput, Dataset, KeywordMatcher, RecordFactory, SourceAdapter,
        add_readme, now_iso, schema_fingerprint, verify_descriptor)

VERSION="0.1.0"
SOURCE="youtube"
VIDEO_NAMESPACE="youtube_video"
COMMENT_NAMESPACE="youtube_comment"
VIDEO_ID=re.compile(r"[A-Za-z0-9_-]{11}")
COMMENT_ID=re.compile(r"[A-Za-z0-9_.-]{1,256}")

def video_url(value):
    try:
        p=urlsplit(value.strip())
        if p.scheme!="https" or p.username or p.password or p.port not in (None,443):raise ValueError()
        host=(p.hostname or "").lower()
        if host in {"youtube.com","www.youtube.com","m.youtube.com"}:
            if p.path=="/watch":ids=parse_qs(p.query).get("v",[]);vid=ids[0] if len(ids)==1 else ""
            else:
                match=re.fullmatch(r"/(?:shorts|live)/([A-Za-z0-9_-]{11})/?",p.path)
                vid=match[1] if match else ""
        elif host=="youtu.be":vid=p.path.strip("/")
        else:raise ValueError()
        if not VIDEO_ID.fullmatch(vid):raise ValueError()
        return f"https://www.youtube.com/watch?v={vid}"
    except ValueError as exc:
        raise ValueError("Gunakan permalink video HTTPS youtube.com/watch, /shorts/, /live/ atau youtu.be; URL kanal bukan input video.") from exc

def error_code(message):
    text=str(message).lower()
    if any(x in text for x in ("certificate verify failed","certificate_verify_failed")):return "TLS_ERROR"
    if "429" in text or "too many requests" in text:return "RATE_LIMITED"
    if any(x in text for x in ("sign in","login required","confirm you’re not a bot","confirm you're not a bot","captcha")):return "LOGIN_OR_CHALLENGE"
    if "403" in text or "forbidden" in text:return "ACCESS_BLOCKED"
    if "comments are disabled" in text or "comments disabled" in text:return "COMMENTS_DISABLED"
    if "private video" in text or "members-only" in text:return "PRIVATE_TARGET"
    if "timed out" in text or "timeout" in text:return "NETWORK_TIMEOUT"
    return "UPSTREAM_ERROR"

class SafeLogger:
    def __init__(self):self.codes=set()
    def debug(self,message):pass
    def info(self,message):pass
    def warning(self,message):
        if len(self.codes)<32:self.codes.add(error_code(message))
    def error(self,message):self.warning(message)

@dataclass(frozen=True, slots=True)
class Settings:
    project_id:str="university-intelligence"
    max_videos:int=3
    search_results:int=3
    max_comments:int=100
    max_replies:int=30
    max_replies_per_thread:int=5
    timeout_seconds:int=120
    total_seconds:int=600
    request_delay:float=2.0
    sort:str="new"
    cert_store:str="system"
    since:str|None=None
    until:str|None=None
    keywords:tuple[str,...]=("BINUS","universitas","kampus","biaya kuliah","beasiswa","jurusan")

    def validate(self):
        limits={"max_videos":(1,20),"search_results":(1,10),"max_comments":(1,2000),"max_replies":(0,1000),
                "max_replies_per_thread":(0,100),"timeout_seconds":(10,600),"total_seconds":(20,3600)}
        for k,(a,b) in limits.items():
            v=getattr(self,k)
            if type(v) is not int or not a<=v<=b:raise ValueError(f"{k} harus integer {a}–{b}")
        if type(self.request_delay) not in (int,float) or not 0<=self.request_delay<=30:raise ValueError("request_delay harus 0–30 detik")
        if self.sort not in {"new","top"} or self.cert_store not in {"system","bundled"}:raise ValueError("sort/cert_store tidak dikenal")
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}",self.project_id):raise ValueError("project_id harus slug 1–100 karakter")
        if not isinstance(self.keywords,(list,tuple)) or any(not isinstance(k,str) for k in self.keywords):raise ValueError("keywords harus daftar string")
        KeywordMatcher(self.keywords)

def worker(operation,target,settings,pipe):
    # Only sanitized, selected fields leave this process. No cookies or credentials.
    if os.name=="posix":os.setsid()
    try:
        import yt_dlp
        from yt_dlp.version import __version__
        logger=SafeLogger()
        opts={"quiet":True,"noprogress":True,"logger":logger,"skip_download":True,"noplaylist":True,
              "cachedir":False,"socket_timeout":15,"retries":0,"extractor_retries":0,"fragment_retries":0,
              "nocheckcertificate":False,"ignore_no_formats_error":True,"ignoreerrors":False,
              "getcomments":operation=="video","extract_flat":operation=="search"}
        if settings["cert_store"]=="system":opts["compat_opts"]={"no-certifi"}
        limits=[settings["max_comments"],settings["max_comments"],settings["max_replies"],settings["max_replies_per_thread"],2]
        opts["extractor_args"]={"youtube":{"comment_sort":[settings["sort"]],"max_comments":[str(x) for x in limits]}}
        with yt_dlp.YoutubeDL(opts) as ydl:
            if operation=="search":
                info=ydl.extract_info(f"ytsearch{settings['search_results']}:{target}",download=False)
                if not info:raise RuntimeError("No search result object")
                found=0
                for n,entry in enumerate(info.get("entries") or []):
                    if n>=settings["search_results"]:break
                    if entry and isinstance(entry.get("id"),str) and VIDEO_ID.fullmatch(entry["id"]):
                        found+=1
                        pipe.send(("candidate",{"url":f"https://www.youtube.com/watch?v={entry['id']}",
                            "discovered_from":"https://www.youtube.com/results?"+urlencode({"search_query":target})}))
                pipe.send(("done",{"status":"FINISHED_BEST_EFFORT" if found else "NO_RESULT_UNKNOWN","reason":"bounded_search_results_not_exhaustive" if found else "no_video_candidates_returned",
                    "warnings":sorted(logger.codes),"source_version":__version__}))
            else:
                # Metadata is emitted before comment extraction; it survives comment timeout.
                raw=ydl.extract_info(target,download=False,process=False)
                if not raw or not isinstance(raw.get("id"),str) or not VIDEO_ID.fullmatch(raw["id"]):raise RuntimeError("No video ID")
                if raw.get("availability") in {"private","premium_only","subscriber_only","needs_auth"}:
                    pipe.send(("done",{"status":"PRIVATE_TARGET","reason":"public_video_required","warnings":[],"source_version":__version__}));return
                selected={k:raw.get(k) for k in ("id","title","description","timestamp","upload_date","channel_id","channel_url","comment_count","view_count","like_count","availability")}
                pipe.send(("video",selected))
                result=ydl.process_ie_result(raw,download=False)
                comments=result.get("comments")
                if not isinstance(comments,list):
                    pipe.send(("done",{"status":"NO_RESULT_UNKNOWN","reason":"comments_field_missing_not_zero_comments",
                        "warnings":sorted(logger.codes),"source_version":__version__}));return
                for c in comments[:settings["max_comments"]]:
                    if not isinstance(c,dict):continue
                    pipe.send(("comment",{k:c.get(k) for k in ("id","text","parent","timestamp","_time_text","like_count","author_id")}))
                status=("COMMENTS_DISABLED" if "COMMENTS_DISABLED" in logger.codes else
                        "LIMIT_REACHED" if len(comments)>=settings["max_comments"] else
                        "FINISHED_BEST_EFFORT" if comments else "NO_RESULT_UNKNOWN")
                pipe.send(("done",{"status":status,"reason":"bounded_web_comments_not_complete" if comments else "no_comments_returned_not_proof_of_absence",
                    "warnings":sorted(logger.codes),"source_version":__version__}))
    except ImportError:
        pipe.send(("done",{"status":"DEPENDENCY_MISSING","reason":"install_requirements","warnings":[],"source_version":None}))
    except Exception as exc:
        pipe.send(("done",{"status":error_code(exc),"reason":"source_failed_no_raw_error_or_credentials_exported",
            "warnings":[],"source_version":None}))
    finally:pipe.close()

def run_worker(operation,target,settings,seconds,on_event,*,worker_entry=worker):
    context=mp.get_context("spawn");parent,child=context.Pipe(duplex=False)
    proc=context.Process(target=worker_entry,args=(operation,target,asdict(settings),child));proc.start();child.close()
    deadline=time.monotonic()+seconds;result=None
    try:
        while time.monotonic()<deadline:
            if parent.poll(min(0.2,max(0,deadline-time.monotonic()))):
                try:kind,payload=parent.recv()
                except EOFError:break
                if kind=="done":result=payload;break
                on_event(kind,payload)
            elif not proc.is_alive():
                if parent.poll():continue
                break
        return result or {"status":"TIMEOUT" if proc.is_alive() else "WORKER_FAILED",
            "reason":"hard_deadline_partial_events_preserved" if proc.is_alive() else "worker_exited_without_receipt",
            "warnings":[],"source_version":None}
    finally:
        parent.close();proc.join(timeout=0.5)
        if proc.is_alive():
            if os.name=="posix":
                try:
                    if os.getpgid(proc.pid)==proc.pid:os.killpg(proc.pid,signal.SIGTERM)
                    else:proc.terminate()
                except ProcessLookupError:pass
            else:proc.terminate()
            proc.join(timeout=1)
            if proc.is_alive():proc.kill();proc.join(timeout=1)

class YouTubeAdapter(SourceAdapter):
    def __init__(self,factory,dataset,version):self.factory,self.dataset,self.version=factory,dataset,version

    def accept(self,kind,raw,url,discovered_from):
        vid=parse_qs(urlsplit(url).query)["v"][0]
        root=self.factory.key(SOURCE,VIDEO_NAMESPACE,vid)
        common=dict(platform=SOURCE,namespace=VIDEO_NAMESPACE if kind=="video" else COMMENT_NAMESPACE,page_url=url,thread_root_key=root,
            discovered_from=discovered_from,extraction_method="yt_dlp_unofficial_web",adapter_version="youtube-adapter:"+VERSION+";yt-dlp:"+self.version)
        if kind=="video":
            if raw.get("id")!=vid:raise ValueError("Video ID tidak cocok dengan target")
            stamp=None;quality="unknown";flags=["video_context_only","bounded_web_view"]
            if type(raw.get("timestamp")) in (int,float):
                try:stamp=datetime.fromtimestamp(raw["timestamp"],timezone.utc).isoformat();quality="exact"
                except (ValueError,OverflowError,OSError):flags.append("invalid_source_timestamp")
            if stamp is None and raw.get("upload_date"):quality="date_only";flags.append("publication_timezone_unknown")
            record=ContentInput(**common,native_id=vid,object_type="post",canonical_url=url,title=raw.get("title"),
                text_source=raw.get("description") or "",publisher_ref=raw.get("channel_url"),published_at=stamp,
                published_display=str(raw["upload_date"]) if raw.get("upload_date") else None,timestamp_quality=quality,quality_flags=tuple(flags))
            metrics=[(k,raw.get(k),"count") for k in ("view_count","like_count","comment_count")]
        else:
            cid=raw.get("id")
            if not isinstance(cid,str) or not COMMENT_ID.fullmatch(cid) or not isinstance(raw.get("text"),str):raise ValueError("Schema komentar berubah")
            parent=raw.get("parent");flags=["bounded_web_view","hidden_comments_unknown"]
            if parent=="root":parent_key=root;kind="comment"
            elif isinstance(parent,str) and COMMENT_ID.fullmatch(parent):parent_key=self.factory.key(SOURCE,COMMENT_NAMESPACE,parent);kind="reply"
            else:parent_key=None;kind="comment";flags.append("parent_unknown_not_assumed_root")
            # yt-dlp explicitly estimates comment timestamps from relative UI text.
            # Never copy that estimate into the exact published_at column.
            display=raw.get("_time_text")
            quality="relative" if isinstance(display,str) and display else "unknown"
            flags.append("upstream_comment_timestamp_is_estimate")
            record=ContentInput(**common,native_id=cid,object_type=kind,parent_key=parent_key,
                canonical_url=url+"&lc="+quote(cid,safe=""),text_source=raw["text"],published_at=None,
                published_display=display if isinstance(display,str) else None,timestamp_quality=quality,
                author_native_id=raw.get("author_id"),quality_flags=tuple(flags))
            metrics=[("like_count",raw.get("like_count"),"count")]
        return self.dataset.add_content(record,metrics)

def load_settings(args):
    data={}
    if args.config:
        if args.config.stat().st_size>1_000_000:raise ValueError("Config terlalu besar")
        data=json.loads(args.config.read_text(encoding="utf-8"))
        if not isinstance(data,dict):raise ValueError("Config harus JSON object")
    known=set(Settings.__dataclass_fields__)|{"urls","queries"}
    if set(data)-known:raise ValueError("Config memuat field tidak dikenal: "+", ".join(sorted(set(data)-known)))
    urls=data.pop("urls",[]);queries=data.pop("queries",[])
    for key in Settings.__dataclass_fields__:
        value=getattr(args,key,None)
        if value is not None:data[key]=value
    if args.keyword:data["keywords"]=tuple(args.keyword)
    settings=Settings(**data);settings.validate()
    if not isinstance(urls,list) or not isinstance(queries,list) or any(not isinstance(v,str) for v in urls+queries):raise ValueError("urls/queries harus daftar string")
    urls+=args.url or [];queries+=args.query or []
    if args.urls_file:
        if args.urls_file.stat().st_size>1_000_000:raise ValueError("File URL terlalu besar")
        urls.extend(l.strip() for l in args.urls_file.read_text(encoding="utf-8-sig").splitlines() if l.strip() and not l.lstrip().startswith("#"))
    urls=list(dict.fromkeys(video_url(u) for u in urls));queries=list(dict.fromkeys(q.strip() for q in queries if q.strip()))
    if len(urls)>100 or len(queries)>10 or any(len(q)>300 or any(ord(c)<32 for c in q) for q in queries):raise ValueError("Maksimum 100 URL dan 10 query, masing-masing 300 karakter")
    if not urls and not queries:raise ValueError("Isi --url, --query, --urls-file atau config")
    return settings,urls,queries

def run(args):
    verify_descriptor();settings,urls,queries=load_settings(args)
    run_id=str(uuid.uuid4());factory=RecordFactory(settings.project_id,run_id,KeywordMatcher(settings.keywords),settings.since,settings.until)
    output=args.output_dir or Path("output")/("youtube_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"_"+run_id[:8])
    sink=BundleSink(output,settings.project_id,run_id);dataset=Dataset(factory,sink)
    try:version=importlib.metadata.version("yt-dlp")
    except importlib.metadata.PackageNotFoundError:version="not_installed"
    adapter=YouTubeAdapter(factory,dataset,version);deadline=time.monotonic()+settings.total_seconds
    failures=0;interrupted=False;receipts=[]

    def execute(operation,target,callback):
        nonlocal failures
        started=now_iso();before=dataset.contents;dupes=dataset.duplicates;counts={"comment":0,"reply":0,"invalid":0}
        def receive(kind,payload):
            if kind=="comment":counts["reply" if payload.get("parent") not in (None,"root") else "comment"]+=1
            try:callback(kind,payload)
            except (ValueError,TypeError,OverflowError):counts["invalid"]+=1
        remaining=deadline-time.monotonic()
        if remaining<=0:result={"status":"SKIPPED_GLOBAL_DEADLINE","reason":"global_budget_exhausted","warnings":[],"source_version":version}
        else:
            print(f"{operation}: {target}",flush=True)
            try:result=run_worker(operation,target,settings,min(settings.timeout_seconds,remaining),receive)
            except KeyboardInterrupt:result={"status":"INTERRUPTED","reason":"user_interrupted_partial_events_preserved","warnings":[],"source_version":version}
        if counts["invalid"]:result={**result,"status":"PARTIAL_SCHEMA_ERROR","reason":"some_source_rows_rejected","warnings":[*result["warnings"],"invalid_source_rows"]}
        status=result["status"]
        if status not in {"FINISHED_BEST_EFFORT","LIMIT_REACHED"}:failures+=1
        row=factory.row("Runs",unit_id=str(uuid.uuid4()),source=SOURCE,operation=operation,target=target,status=status,
            reason=result["reason"],coverage="PARTIAL_UNKNOWN_TOTAL",contents_written=dataset.contents-before,
            comments_seen=counts["comment"],replies_seen=counts["reply"],duplicates_skipped=dataset.duplicates-dupes,
            invalid_rows=counts["invalid"],max_comments=settings.max_comments if operation=="video" else None,
            max_replies=settings.max_replies if operation=="video" else None,timeout_seconds=settings.timeout_seconds,
            keywords=list(settings.keywords),source_version=result["source_version"],warning_codes=result["warnings"],started_at=started,finished_at=now_iso())
        sink.write("Runs",row);receipts.append(row)
        print(f"  {status}; {row['contents_written']} content rows",flush=True)
        if status=="INTERRUPTED":raise KeyboardInterrupt

    try:
        targets={u:None for u in urls[:settings.max_videos]}
        for query in queries:
            if len(targets)>=settings.max_videos:
                sink.write("Runs",factory.row("Runs",unit_id=str(uuid.uuid4()),source=SOURCE,operation="search",target=query,
                    status="SKIPPED_VIDEO_LIMIT",reason="video_budget_already_full",coverage="NOT_RUN",contents_written=0,comments_seen=0,
                    replies_seen=0,duplicates_skipped=0,invalid_rows=0,max_comments=None,max_replies=None,timeout_seconds=settings.timeout_seconds,
                    keywords=list(settings.keywords),source_version=version,warning_codes=[],started_at=now_iso(),finished_at=now_iso()))
                continue
            def candidate(kind,payload):
                if kind=="candidate" and len(targets)<settings.max_videos:
                    targets.setdefault(video_url(payload["url"]),payload["discovered_from"])
            execute("search",query,candidate)
            if time.monotonic()<deadline:time.sleep(min(settings.request_delay,max(0,deadline-time.monotonic())))
        for url in urls[settings.max_videos:]:
            sink.write("Runs",factory.row("Runs",unit_id=str(uuid.uuid4()),source=SOURCE,operation="video",target=url,status="SKIPPED_VIDEO_LIMIT",
                reason="video_budget_already_full",coverage="NOT_RUN",contents_written=0,comments_seen=0,replies_seen=0,duplicates_skipped=0,
                invalid_rows=0,max_comments=settings.max_comments,max_replies=settings.max_replies,timeout_seconds=settings.timeout_seconds,
                keywords=list(settings.keywords),source_version=version,warning_codes=[],started_at=now_iso(),finished_at=now_iso()))
        for url,origin in targets.items():
            execute("video",url,lambda kind,payload,u=url,o=origin:adapter.accept(kind,payload,u,o))
            if time.monotonic()<deadline:time.sleep(min(settings.request_delay,max(0,deadline-time.monotonic())))
    except KeyboardInterrupt:
        interrupted=True;failures+=1
    try:
        dataset.finish_relations()
        sink.write("Sources",factory.row("Sources",source=SOURCE,producer_version=VERSION,upstream_version=version,
            extraction_method="yt_dlp_unofficial_web",access_mode="guest_no_cookies",config={**asdict(settings),"urls":urls,"queries":queries},
            schema_fingerprint=schema_fingerprint(),observed_at=now_iso()))
        add_readme(sink,factory,[("YouTube","Video/audio tidak diunduh. Hanya metadata dan komentar publik yang dapat diakses; live chat tidak termasuk."),
            ("Komentar YouTube","Timestamp hasil yt-dlp berasal dari teks waktu relatif; published_at dibiarkan null. Bila memakai filter tanggal, komentar seperti ini masuk review."),
            ("Timeout","Metadata yang sudah dikirim dipertahankan. yt-dlp membuffer komentar; timeout sebelum selesai dapat menghasilkan nol komentar meski sumber memiliki komentar."),
            ("Hasil run",f"contents={dataset.contents}, duplicates={dataset.duplicates}, failed_units={failures}, interrupted={interrupted}")])
        sink.finish({"source":SOURCE,"producer_version":VERSION,"mode":"live_guest_web","synthetic":False,"failed_units":failures,
            "interrupted":interrupted,"limitations":["bounded_non_exhaustive_search","unknown_comment_coverage","relative_comment_dates","no_actor_inference","no_sentiment_labels","no_supabase_transfer"]})
    except BaseException:sink.abort();raise
    print("Output: "+str(sink.path),flush=True)
    return 130 if interrupted else 2 if failures else 0

def parser():
    p=argparse.ArgumentParser(description=__doc__)
    subs=p.add_subparsers(dest="command",required=True)
    subs.add_parser("contract",help="Validasi contract.json dan tampilkan fingerprint")
    subs.add_parser("doctor",help="Periksa dependensi, tanpa mengakses YouTube")
    r=subs.add_parser("run",help="Crawl YouTube ke Excel dan JSONL dengan format bersama")
    r.add_argument("--config",type=Path);r.add_argument("--output-dir",type=Path)
    r.add_argument("--url",action="append");r.add_argument("--query",action="append");r.add_argument("--urls-file",type=Path)
    r.add_argument("--keyword",action="append");r.add_argument("--project-id")
    for name in ("max_videos","search_results","max_comments","max_replies","max_replies_per_thread","timeout_seconds","total_seconds"):
        r.add_argument("--"+name.replace("_","-"),type=int)
    r.add_argument("--request-delay",type=float);r.add_argument("--sort",choices=["new","top"])
    r.add_argument("--cert-store",choices=["system","bundled"]);r.add_argument("--since");r.add_argument("--until")
    return p

def main():
    args=parser().parse_args()
    try:
        if args.command=="contract":verify_descriptor();print(schema_fingerprint());return 0
        if args.command=="doctor":
            print("Python:",sys.version.split()[0])
            for pkg in ("openpyxl","yt-dlp"):
                try:print(pkg+":",importlib.metadata.version(pkg))
                except importlib.metadata.PackageNotFoundError:print(pkg+": MISSING")
            verify_descriptor();print("Contract:",schema_fingerprint());print("Doctor tidak membuktikan akses live.");return 0
        return run(args)
    except (ValueError,FileNotFoundError,FileExistsError,json.JSONDecodeError) as exc:
        print("Input/contract error: "+str(exc),file=sys.stderr);return 2

if __name__=="__main__":
    mp.freeze_support();raise SystemExit(main())
