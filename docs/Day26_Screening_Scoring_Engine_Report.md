

\# Day 26 – Screening Scoring Engine Report



\## 1. Overview



The Day 26 Screening Scoring Engine evaluates candidate screening answers using four scoring parameters:



\- Clarity

\- Relevance

\- Completeness

\- Consistency



The engine generates individual question scores, weighted scores, an overall screening score, and explanations for each scoring decision.



\## 2. Scoring Parameters and Weights



| Parameter | Weight |

|---|---:|

| Clarity | 25% |

| Relevance | 30% |

| Completeness | 25% |

| Consistency | 20% |

| \*\*Total\*\* | \*\*100%\*\* |



The weights are configurable through `scoring\_config.py`.



\## 3. Scoring Methodology



\### Clarity

Evaluates answer length and basic communication clarity using a word-count heuristic.



\### Relevance

Uses the Day 25 Answer Understanding Engine output to identify missing, vague, and off-topic answers.



\### Completeness

Checks whether required information is present and whether the answer is missing, vague, or off-topic.



\### Consistency

Performs basic validation of extracted experience, salary, and availability values, including checks for negative values.



\## 4. Weighted Score Calculation



Each parameter receives a score between 0 and 100.



The weighted score is calculated as:



Weighted Score =

(Clarity × 0.25) +

(Relevance × 0.30) +

(Completeness × 0.25) +

(Consistency × 0.20)



The final score is normalized to the range of 0–100.



\## 5. Overall Screening Score



The overall screening score is calculated as the arithmetic mean of the individual question scores.



Performance categories:



| Score Range | Performance Level |

|---|---|

| 80–100 | Excellent |

| 65–79.99 | Good |

| 50–64.99 | Average |

| Below 50 | Needs Improvement |



\## 6. Implementation Files



\- `src/screening\_scoring/scoring\_config.py`

\- `src/screening\_scoring/question\_scorer.py`

\- `src/screening\_scoring/screening\_scoring\_engine.py`

\- `src/screening\_scoring/scoring\_pipeline.py`

\- `testing/day26/test\_day26\_scoring.py`



\## 7. Generated Output



Output file:



`data/processed/day26/screening\_scoring\_results.json`



The output contains:



\- Total number of questions evaluated

\- Overall screening score

\- Performance level

\- Individual question breakdown

\- Four parameter scores per question

\- Scoring weights

\- Explanations for each parameter

\- Average scores for each parameter



\## 8. Test Results



Day 26 automated tests:



\*\*9 tests passed\*\*



The tests cover:



\- Complete answer scoring

\- Missing answer scoring

\- Off-topic answer relevance

\- Off-topic answer completeness

\- Vague answer completeness

\- Score normalization

\- Overall screening score calculation

\- Empty screening results

\- Per-question explanations



\## 9. Sample Execution Results



Total questions evaluated: 6



Overall screening score: 75.00/100



Performance level: Good



Parameter averages:



| Parameter | Average Score |

|---|---:|

| Clarity | 73.33 |

| Relevance | 66.67 |

| Completeness | 66.67 |

| Consistency | 100.00 |



Individual question scores:



| Question ID | Score |

|---|---:|

| Q001 | 100 |

| Q002 | 100 |

| Q003 | 90 |

| Q004 | 90 |

| Q005 | 35 |

| Q006 | 35 |



\## 10. Limitations



\- Clarity is evaluated using a basic word-count heuristic.

\- Relevance and completeness depend on the Day 25 rule-based answer understanding output.

\- Consistency checks currently cover only basic extracted-value validation.

\- Cross-answer consistency and contradictions are not yet comprehensively evaluated.

\- The scoring system is a rule-based baseline, not a trained machine-learning model.

\- Scores should support human screening decisions rather than serve as the sole basis for hiring.



\## 11. Conclusion



The Day 26 Screening Scoring Engine successfully evaluates candidate screening responses using four weighted parameters.



It generates normalized question-level scores, an overall screening score, performance categories, and explainable scoring outputs.



The implementation establishes a foundation for future improvements in semantic evaluation, advanced consistency checking, and automated candidate assessment.



