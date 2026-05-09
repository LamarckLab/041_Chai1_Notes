## Lamarck &nbsp; &nbsp; &nbsp; 2026-05-09
#### 该文档用于展示 Chai-1 输入 FASTA 的常见格式（以蛋白质为例）
---

> **00 普通 FASTA vs Chai-1 FASTA**

普通 FASTA 的 header 完全自由，没有强制结构
```text
>sp|P00533|EGFR_HUMAN Epidermal growth factor receptor OS=Homo sapiens
MRPSGTAGAALLALLAALCPASRALEEKKVCQGTSNKLTQLGTFEDHFLSLQRMFNNCEVVLG
```

Chai-1 FASTA 要求 header 必须显式声明分子类型，统一格式为 `>{type}|name={chain_name}` ，合法的 type 只有 4 个：`protein` / `dna` / `rna` / `ligand` ，多链 / 复合物用多条 record 表达，每条 record 必须独立声明类型，同一个文件里的所有 record 默认会被 Chai-1 当作同一个复合物的不同链共同建模

---

> **01 单链蛋白**
```text
>protein|name=ubiquitin
MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG
```

---

> **02 同源多聚体**
```text
>protein|name=chain_A
MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG
>protein|name=chain_B
MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG
```

---

> **03 异源多聚体**
```text
>protein|name=receptor
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKR
>protein|name=binder
GHYTRMNAEKQPLEMQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQK
```

---

##### [Chai-1官方仓库](https://github.com/chaidiscovery/chai-lab)
