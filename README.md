# Guilherme Luis Morschel (Atividade Presença)

## Como rodar com Docker

```bash
docker build -t exercicios_gui .
docker run --rm -v $(pwd):/workspace -w /workspace exercicios_gui ex_1/main.py
