# Kaggle テンプレ

```text
├── .jupyter-settings: jupyter-lab の設定ファイル。compose.yamlでJUPYTERLAB_SETTINGS_DIRを指定している
├── Dockerfile
├── Dockerfile.cpu
├── README.md
├── compose.cpu.yaml
├── compose.yaml
├── config
    ├── env
        ├── kaggle
        ├── local
    ├── base.yaml
    ├── exp001
├── input
├── src
    ├── notebook
    ├── utils
├── output
    ├── expname

```

## Docker による環境構築
```sh
#コンペ名に変える
git clone https://github.com/moon0808/kaggle_template.git titanic(compe name)
```

ローカルPCなら
```sh
docker compose -f compose.cpu.yaml build
docker compose -f compose.cpu.yaml up -d
```

GPUサーバなら
```sh
docker compose -f compose.yaml build
docker compose -f compose.yaml up -d
```

基本的にはここから
```sh
docker compose run --rm kaggle bash

# jupyter lab を起動する場合
docker compose up 
```

コマンドパレットで
** Remote-Containers: Attach to Running Container **

