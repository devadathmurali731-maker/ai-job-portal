

\# Day 27 – Confidence and Sentiment Signal Analysis Report



\## 1. Overview



The Day 27 Confidence and Sentiment Signal Analysis module evaluates candidate communication signals and behavioral indicators from structured screening answers.



The system analyzes:



\- Text-based hesitation patterns

\- Uncertainty expressions

\- Response length

\- Speaking pace when audio duration is available

\- Positive and negative sentiment

\- Potential contradictions across extracted answers

\- Communication strength indicators



\## 2. Implementation Modules



\### Confidence Analysis

File: `src/confidence\_analysis/confidence\_analyzer.py`



Evaluates confidence using:

\- Hesitation phrase frequency

\- Uncertainty phrase frequency

\- Response length

\- Day 25 intent confidence

\- Answer status



Produces a confidence score from 0 to 100 and a confidence level.



\### Sentiment Analysis

File: `src/sentiment\_analysis/sentiment\_scorer.py`



Uses predefined positive and negative vocabulary.



Sentiment scores range from 0 to 100:

\- 60–100: Positive

\- 41–59: Neutral

\- 0–40: Negative



\### Contradiction Detection

File: `src/confidence\_analysis/contradiction\_detector.py`



Compares extracted experience, salary, and availability values across candidate answers.



Differences are flagged as potential contradictions and require human review.



\### Communication Analysis Engine

File: `src/confidence\_analysis/communication\_analyzer.py`



Combines confidence, sentiment, hesitation, uncertainty, and contradiction analysis.



\### Execution Pipeline

File: `src/confidence\_analysis/communication\_pipeline.py`



Reads Day 25 structured answers and generates the Day 27 behavioral indicators report.



\## 3. Communication Strength Indicators



Communication strength is categorized using average confidence:



| Confidence Score | Communication Strength |

|---|---|

| 80–100 | Strong |

| 60–79.99 | Moderate |

| Below 60 | Needs Improvement |



These are heuristic indicators, not psychological assessments.



\## 4. Response Length and Pace



Response length is measured using:

\- Word count

\- Character count

\- Length category



Speaking pace is calculated in words per minute when transcript duration is provided:



Words per minute = Word count / Duration in minutes



When audio duration is unavailable, the system records the pace as unavailable rather than estimating it.



\## 5. Sample Execution Results



Total answers analyzed: 6



Average confidence score: 73.84/100



Average sentiment score: 51.67/100



Communication strength: Moderate



Behavioral indicators:



| Indicator | Result |

|---|---:|

| Hesitation instances | 1 |

| Uncertainty instances | 1 |

| Potential contradictions | 0 |



\## 6. Individual Confidence Results



| Answer ID | Confidence Score | Level |

|---|---:|---|

| A001 | 85.00 | High |

| A002 | 80.05 | High |

| A003 | 85.00 | High |

| A004 | 85.00 | High |

| A005 | 43.00 | Low |

| A006 | 65.00 | Moderate |



\## 7. Sample Sentiment Results



| Answer ID | Sentiment Score | Label |

|---|---:|---|

| A001 | 60 | Positive |

| A002 | 50 | Neutral |

| A003 | 50 | Neutral |

| A004 | 50 | Neutral |

| A005 | 50 | Neutral |

| A006 | 50 | Neutral |



\## 8. Generated Output



Output file:



`data/processed/day27/behavioral\_indicators\_report.json`



The report contains:

\- Average confidence and sentiment

\- Individual answer analysis

\- Hesitation and uncertainty counts

\- Response length and pace fields

\- Potential contradiction results

\- Communication strength

\- Method limitations



\## 9. Testing



Automated test file:



`testing/day27/test\_day27\_analysis.py`



Test coverage includes:

\- Confidence analysis

\- Hesitation detection

\- Uncertainty detection

\- Response length measurement

\- Positive sentiment

\- Negative sentiment

\- Neutral sentiment

\- Contradiction detection

\- No-contradiction handling

\- Combined communication analysis



Test result: 10 tests passed.



\## 10. Limitations



\- Confidence scores are rule-based communication signals, not psychological measurements.

\- Sentiment analysis uses a predefined vocabulary and may miss context, sarcasm, or negation.

\- Speaking pace requires audio duration.

\- Vocal hesitation and pauses require acoustic or timestamp analysis.

\- Different extracted values are potential conflicts, not necessarily genuine contradictions.

\- Communication strength should not be used as the sole basis for candidate selection.



\## 11. Conclusion



The Day 27 implementation successfully combines text-based confidence analysis, sentiment scoring, hesitation detection, response length measurement, and potential contradiction detection.



It generates explainable behavioral indicators for candidate screening and establishes a foundation for future audio-based communication analysis.



