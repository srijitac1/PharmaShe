#!/bin/bash
LOGFILE=train_doc_chunks_trainer_v3_$(date +%Y%m%d_%H%M%S).log

export TORCH_NCCL_ASYNC_ERROR_HANDLING=1
export NCCL_P2P_LEVEL=NVL
export NCCL_IB_DISABLE=1        # When IB is not used/unstable

export TORCH_LOAD_WEIGHTS_ONLY=0
export TOKENIZERS_PARALLELISM=false

# export TRANSFORMERS_CACHE=/localssd/hf
# export HF_HOME=/localssd/hf
# export HF_DATASETS_CACHE=/localssd/hf_ds
export HF_DATASETS_CACHE=/scratch/sbms003/sji/hf_cache
#export HF_HOME=/group/sbms003/sji/hf_home

torchrun --nproc_per_node=2 train_doc_chunks_trainer_v3.py \
  --args ... \
  2>&1 | tee $LOGFILE
