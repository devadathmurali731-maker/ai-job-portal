\# Day 24 – Speech-to-Text Accuracy Report



\## 1. Objective

Integrate speech-to-text using OpenAI Whisper and verify transcription of audio input.



\## 2. Test Environment

\- Model: `openai/whisper-base`

\- Framework: Hugging Face Transformers

\- Execution device: CPU

\- Audio library: SoundFile

\- Resampling: SciPy `resample\_poly`

\- Required model sample rate: 16,000 Hz



\## 3. Test Audio

\- File: `data/processed/day24/test\_speech.wav`

\- Audio source: Synthetic speech generated using Windows System.Speech

\- Voice: Microsoft Zira Desktop

\- Original sample rate: 22,050 Hz

\- Reference transcript: "Hello, my name is Alex. I have three years of experience in data analysis and Python programming."



\## 4. Observed Output

"Hello, my name is Alex. I have three years of experience in data analysis and Python programming."



\## 5. Accuracy Results

\- Reference word count: 17

\- Substitutions: 0

\- Deletions: 0

\- Insertions: 0

\- Word Error Rate (WER): 0%

\- Word accuracy for this sample: 100%



Formula: WER = (Substitutions + Deletions + Insertions) / Reference Word Count



\## 6. Automated Testing

\- Day 24 tests passed: 24

\- Failures: 0

\- Verified areas include transcript normalization, transcript processing, silence handling, missing audio handling, and lazy model loading.



\## 7. Limitations

The current accuracy result represents one synthetic English speech sample. It does not establish performance across multiple accents, background noise, interrupted speech, or partial answers. These require additional representative audio samples and separate measurements.



\## 8. Conclusion

The Whisper integration successfully transcribed the test audio. The implementation supports mono conversion, silence detection, and resampling to 16 kHz. Further testing is required before claiming robust performance across accents and noisy conditions.



