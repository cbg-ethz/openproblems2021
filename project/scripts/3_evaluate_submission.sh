#!/bin/bash

set -e

# change these parameters if need be
PIPELINE_VERSION="1.2.0"

# ViashSourceDir: return the path of a bash file, following symlinks
# usage   : ViashSourceDir ${BASH_SOURCE[0]}
# $1      : Should always be set to ${BASH_SOURCE[0]}
# returns : The absolute path of the bash file
function ViashSourceDir {
  SOURCE="$1"
  while [ -h "$SOURCE" ]; do
    DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
  done
  cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd
}

# cd to root dir of starter kit
cd `ViashSourceDir ${BASH_SOURCE[0]}`/..

# checking environment
scripts/0_sys_checks.sh


echo ""
echo "######################################################################"
echo "##                      Evaluating predictions                      ##"
echo "######################################################################"

export NXF_VER=21.04.1

bin/nextflow run \
  openproblems-bio/neurips2021_multimodal_viash \
  -r $PIPELINE_VERSION \
  -main-script src/predict_modality/workflows/evaluate_submission/main.nf \
  --solutionDir 'output/datasets/predict_modality' \
  --predictions 'output/predictions/predict_modality/**.h5ad' \
  --publishDir 'output/evaluation/predict_modality' \
  -resume \
  -latest


# print message
echo ""
echo "######################################################################"
echo "##                        Evaluation summary                        ##"
echo "######################################################################"
echo "Evaluation results are stored at 'output/evaluation/predict_modality'."