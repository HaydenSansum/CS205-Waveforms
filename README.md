# CS205-Waveforms

## Examples

Train:
```
python train.py --data_dir='../songs/wav' --num_steps 10
```

Generate:
For generation you need to specify the latest checkpoint for the model geenrated in training, in this example that is the filepath ending ckpt-9
```
python generate.py --wav_out_path=generated.wav --samples 16000 logdir/train/2020-04-20T17-45-36/model.ckpt-9
```

## References:

### ibab-wavenet

All code within the ibab-wavenet folder is clones from the following repository: 
https://github.com/ibab/tensorflow-wavenet

We are using this as our benchmark model to understand the flow of the model and benchmark timing.

Please see the Licensing file within the subfolder for details.

