# Core Algorithms

## Reciprocal skill compatibility

For students A and B, a match is eligible only if:
- A teaches at least one skill B wants to learn; **and**
- B teaches at least one skill A wants to learn.

This avoids one-sided recommendations that cannot form an exchange.

## Compatibility score

For an eligible reciprocal pair:

`Score = 0.70 × SkillFit + 0.20 × AvailabilityFit + 0.10 × ModeFit`

- `SkillFit = 100` when reciprocal skill compatibility exists; otherwise the pair is excluded.
- `AvailabilityFit = 100` when availability labels match, otherwise 60.
- `ModeFit = 100` when learning modes match, otherwise 70.

Scores are between 0 and 100. Candidates are sorted descending using `Match::operator>`.

This is a deterministic rule-based scoring heuristic, not a trained predictive model. The weights are design choices for a student project and could be calibrated using user feedback in future work.

## Search overloads

`StudentService::searchStudents` supports:
- `searchStudents(name)` — partial, case-insensitive name match.
- `searchStudents(name, course)` — name plus course.
- `searchStudents(name, year)` — name plus year.

The compiler selects the overload based on the argument types/count.

## Exchange lifecycle

A request is created with status `Pending` and a date. The recipient can change it to `Accepted` or `Declined`. The update operation rewrites the CSV with the changed status.
