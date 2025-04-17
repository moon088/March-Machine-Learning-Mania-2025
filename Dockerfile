# Dockerfile (GPU対応: CUDA 11.7 + cuDNN8 + Ubuntu22.04)
FROM nvidia/cuda:11.7.0-cudnn8-runtime-ubuntu22.04


RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    ca-certificates \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip


# ruff がnotebook上で設定できないのでblackとisortを入れる
RUN python3 -m pip install --upgrade pip \
    &&  pip install --no-cache-dir \
    black isort \ 
    jupyterlab_code_formatter 


RUN pip install --no-cache-dir \
    hydra-core 
RUN pip install psutil


RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scipy \
    numexpr==2.8.4 \
    scikit-learn \
    matplotlib \
    seaborn \
    plotly \
    tqdm \
    joblib \
    ipywidgets

# 深層学習関連ライブラリ
RUN pip install --no-cache-dir \
    tensorflow \
    keras \
    torch \
    torchvision \
    torchaudio \
    segmentation-models-pytorch \
    xgboost \
    lightgbm \
    catboost \
    opencv-python-headless