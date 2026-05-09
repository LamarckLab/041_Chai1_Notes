## Lamarck &nbsp; &nbsp; &nbsp; 2026-05-09
#### 该文档使用 conda & pip 部署 Chai-1
---

## 01  创建 conda 环境
```bash
conda create -n lmk_chai1 python=3.11 -y --solver=classic
conda activate lmk_chai1
```

## 02  配置权重缓存目录
> 把环境变量绑到 conda env 的激活钩子，激活环境时自动生效，让后续 chai-1 权重下载到 **/data/lmk/chai1_downloads**
```bash
mkdir -p /data/lmk/chai1_downloads
```
```bash
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
cat > $CONDA_PREFIX/etc/conda/activate.d/chai_env.sh <<'EOF'
export CHAI_DOWNLOADS_DIR=/data/lmk/chai1_downloads
EOF
source $CONDA_PREFIX/etc/conda/activate.d/chai_env.sh
```

## 03  安装 chai_lab
> 官方推荐固定版本 0.6.1，首次运行时会自动从 chaiassets.com 下载 7 个权重文件到 CHAI_DOWNLOADS_DIR
```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install chai_lab==0.6.1
```

## 04  安装 kalign 3
> Chai-1 在处理结构模板时会调用 kalign 3，这里直接拉源码编译
```bash
conda install -c conda-forge cmake make -y --solver=classic

cd /tmp
git clone https://github.com/TimoLassmann/kalign.git
cd kalign
mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX ..
make -j 4
make install
hash -r
```
验证 kalign 版本
```bash
which kalign
kalign --version
```

## 05  Chai-1 输入输出目录
**236机子路径**  
> 输入目录：/data/lmk/chai1_inputs  
> 输出目录：/data/lmk/chai1_outputs  


##### [Chai-1官方仓库](https://github.com/chaidiscovery/chai-lab)
