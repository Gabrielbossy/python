The Cinema Screening Assignment System

Background:
You're building a pipeline that assigns movie screenings to theater 
screens. Requests come in asynchronously from different booking desks. 
Your script must process these requests, parse the string-based runtimes 
into usable integers, and prevent screen conflicts for the same movie.

The Input:
You receive a list of screening dictionaries and a Set of currently 
active screen IDs.
A valid screening looks like this:
{"screening_id": "S01", "movie_id": "M-401", "screen_id": "SC3", "runtime": "120min", "release_tier": "premiere"}

The Requirements:

1. Functions & Architecture
Write a main function called process_screenings(screening_batch, active_screens).

Write a helper function called parse_runtime(runtime_string) to convert 
strings like "120min" or "2hr" into a standardized integer representing 
minutes. Assume 1 hr = 60min.

2. Control Flow
Before processing, sort the screenings by release_tier. "premiere" 
screenings must be processed first, followed by "standard", and finally 
"matinee".

Iterate through the sorted batch.

If a screening targets a screen_id that does not exist in the 
active_screens set, ignore the screening completely and move to the next 
one.

3. Exceptions
Use try/except blocks to handle the following messy data scenarios:

Missing Keys: Some screenings will be missing the movie_id or runtime 
keys. Catch this and flag the screening_id as "invalid_schema".

Parsing Errors: If the runtime string is malformed (for example, "N/A" or 
a null value), your helper function should throw a ValueError or 
TypeError. Catch this in the main loop and flag the screening_id as 
"parsing_error".

Custom Exception: Define a ScreenConflictError. As you process valid 
screenings, keep track of which screen each movie is being assigned to. A 
single screen can show multiple movies (across different time slots), but 
a single movie cannot be assigned to two different screens in the same 
batch. If a movie is scheduled for a second screen, raise this exception, 
deny the update, and flag the screening_id as "screen_conflict".

4. Data Structures
Maintain a dictionary tracking the final assigned screen for each movie 
(e.g., {"M-401": "SC3"}).

Return a final summary dictionary containing:

"successful_screenings": An integer count of fully applied screenings.

"movie_screens": The dictionary of movies and their newly assigned screens.

"failed_screenings": A nested dictionary grouping failed screening_ids by 
their error reason ("invalid_schema", "parsing_error", "screen_conflict").

Sample Test Data

{
  "active_screens": ["SC1", "SC2", "SC3", "SC4", "SC8"],
  "screening_batch": [
    {"screening_id": "S01", "movie_id": "M-401", "screen_id": "SC3", "runtime": "120min", "release_tier": "standard"},
    {"screening_id": "S02", "movie_id": "M-909", "screen_id": "SC9", "runtime": "90min", "release_tier": "premiere"},
    {"screening_id": "S03", "movie_id": "M-402", "screen_id": "SC1", "runtime": "2hr", "release_tier": "premiere"},
    {"screening_id": "S04", "movie_id": "M-403", "screen_id": "SC2", "release_tier": "matinee"},
    {"screening_id": "S05", "movie_id": "M-404", "screen_id": "SC8", "runtime": "N/A", "release_tier": "standard"},
    {"screening_id": "S06", "movie_id": "M-402", "screen_id": "SC4", "runtime": "100min", "release_tier": "premiere"}
  ]
}