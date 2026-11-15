"""MiMo Audio 7B Instruct smoke test; run with the upstream repo on PYTHONPATH."""
import argparse
import json
import random
import time
import traceback
from pathlib import Path

import torch
import torchaudio
from src.mimo_audio.mimo_audio import MimoAudio

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--model',required=True,help='MiMo-Audio-7B-Instruct directory')
p.add_argument('--tokenizer',required=True,help='MiMo-Audio-Tokenizer directory')
p.add_argument('--output',required=True,help='New results directory')
p.add_argument('--seed',type=int,default=20261115)
a=p.parse_args()
out=Path(a.output);out.mkdir(parents=True,exist_ok=False)
report={'seed':a.seed,'torch':torch.__version__,'cuda':torch.version.cuda,'gpu':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,'results':[]}
def save(): (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def run(name,fn,wave=None):
    if torch.cuda.is_available():torch.cuda.reset_peak_memory_stats()
    start=time.monotonic();row={'name':name}
    try:
        value=fn()
        if torch.cuda.is_available():torch.cuda.synchronize()
        row.update(status='success',text=str(value),seconds=round(time.monotonic()-start,2))
        if torch.cuda.is_available():row.update(peak_allocated_gib=round(torch.cuda.max_memory_allocated()/2**30,3),peak_reserved_gib=round(torch.cuda.max_memory_reserved()/2**30,3))
        if wave:
            data,sr=torchaudio.load(str(wave));row.update(file=str(wave),sample_rate=sr,duration_s=round(data.shape[-1]/sr,2))
    except Exception as e:
        row.update(status='error',error=str(e),traceback=traceback.format_exc(),seconds=round(time.monotonic()-start,2))
        if torch.cuda.is_available():torch.cuda.empty_cache()
    report['results'].append(row);save();print(json.dumps(row,ensure_ascii=False),flush=True)

random.seed(a.seed);torch.manual_seed(a.seed)
if torch.cuda.is_available():torch.cuda.manual_seed_all(a.seed)
started=time.monotonic()
try:model=MimoAudio(a.model,a.tokenizer)
except Exception:
    report['load_error']=traceback.format_exc();report['load_seconds']=round(time.monotonic()-started,2);save();raise
report['load_seconds']=round(time.monotonic()-started,2);save()
zh=out/'question-zh.wav'
run('中文合成',lambda:model.tts_sft('你好，请用两句话介绍本地部署语音模型有哪些好处。',str(zh),instruct='用自然、清晰、平静的普通话说'),zh)
en=out/'example-en.wav'
run('英文合成',lambda:model.tts_sft('Hello, this is an open source speech model running locally.',str(en)),en)
if zh.exists():
    run('中文音频理解',lambda:model.audio_understanding_sft(str(zh),'请用中文复述这段音频说了什么。'))
    answer=out/'reply-zh.wav'
    run('语音对话',lambda:model.spoken_dialogue_sft(str(zh),str(answer),system_prompt='请用简洁自然的中文回答问题。'),answer)
