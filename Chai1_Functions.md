## Lamarck &nbsp; &nbsp; &nbsp; 2026-05-09
#### 该文档用于记录 server 上跑 Chai-1 的命令
---

> **01 蛋白质结构预测 -- |单任务|远程 MSA + 远程 Template|默认参数|**
```bash
CUDA_VISIBLE_DEVICES=3 \
chai-lab fold \
  --use-msa-server \
  --use-templates-server \
  /data/lmk/chai1_inputs/ubiquitin.fasta \
  /data/lmk/chai1_outputs/ubiquitin/
```

> **02 蛋白质结构预测 -- |单任务|无 MSA + 无 Template|默认参数|**

去掉 `--use-msa-server` 和 `--use-templates-server` 进入 Chai-1 默认的 MSA-free 模式：仅依赖内置 ESM-2 embedding 提供进化信号
```bash
CUDA_VISIBLE_DEVICES=3 \
chai-lab fold \
  /data/lmk/chai1_inputs/ubiquitin.fasta \
  /data/lmk/chai1_outputs/ubiquitin/
```

##### [Chai-1官方仓库](https://github.com/chaidiscovery/chai-lab)
