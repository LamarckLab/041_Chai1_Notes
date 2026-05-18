## Lamarck &nbsp; &nbsp; &nbsp; 2026-05-09
#### 该文档用于记录 server 上跑 Chai-1 的各种命令
---

*路径配置*
```bash
输入目录:   /data/lmk/chai1_inputs       # FASTA 输入
输出目录:   /data/lmk/chai1_outputs      # 预测结构 cif + npz 置信度文件
权重缓存:   /data/lmk/chai1_downloads    # 模型权重缓存
```

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

> **03 蛋白质结构预测 -- |单任务|远程 MSA + 远程 Template|自定义候选结构数目|**

加 `--num-diffn-samples 10` 让 Chai-1 采 10 个候选结构（默认 5），时间约线性变长，显存不变
```bash
CUDA_VISIBLE_DEVICES=3 \
chai-lab fold \
  --use-msa-server \
  --use-templates-server \
  --num-diffn-samples 10 \
  /data/lmk/chai1_inputs/ubiquitin.fasta \
  /data/lmk/chai1_outputs/ubiquitin/
```

> **04 蛋白质结构预测 -- |单任务|远程 MSA + 远程 Template|自定义 seed|**

加 `--seed 42` 让扩散采样可复现，实现完全一致的输出
```bash
CUDA_VISIBLE_DEVICES=3 \
chai-lab fold \
  --use-msa-server \
  --use-templates-server \
  --seed 42 \
  /data/lmk/chai1_inputs/ubiquitin.fasta \
  /data/lmk/chai1_outputs/ubiquitin/
```

> **05 蛋白质结构预测 -- |单任务|远程 MSA + 远程 Template|自定义 trunk recycles|**

加 `--num-trunk-recycles 10` 增加 trunk 网络循环次数（默认 3），提高预测质量
```bash
CUDA_VISIBLE_DEVICES=3 \
chai-lab fold \
  --use-msa-server \
  --use-templates-server \
  --num-trunk-recycles 10 \
  /data/lmk/chai1_inputs/ubiquitin.fasta \
  /data/lmk/chai1_outputs/ubiquitin/
```

> [!IMPORTANT]
> **06 蛋白质结构预测 -- |单任务|远程 MSA + 远程 Template|自定义 contact 约束|**



该功能涉及的示例文件见目录 [custom contact constraints](./custom%20contact%20constraints/)

加 `--constraint-path` 引入残基对接触约束（本质 CSV 格式），强制模型按指定 hot-spot 折叠
```bash
CUDA_VISIBLE_DEVICES=3 \
chai-lab fold \
  --use-msa-server \
  --use-templates-server \
  --constraint-path /data/lmk/chai1_inputs/7syz_contact.restraints \
  /data/lmk/chai1_inputs/7syz_complex.fasta \
  /data/lmk/chai1_outputs/7syz_complex/
```

##### [Chai-1官方仓库](https://github.com/chaidiscovery/chai-lab)
