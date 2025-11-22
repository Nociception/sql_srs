-- themes: case_when count group_by avg percentage
-- tables: season
-- subject: For each division (Div), display the win rate when Lille is at home, and when Lille is away. Read the notes_season.txt file.
-- TODO: Add a feature to display additionnal notes if necessary.

SELECT
    Div,
    AVG (
        CASE 
            WHEN HomeTeam = 'Lille' AND FTHG > FTAG THEN 1
            WHEN HomeTeam = 'Lille' AND FTHG <= FTAG THEN 0
        END
    ) AS lille_wins_home,
    AVG (
        CASE 
            WHEN AwayTeam = 'Lille' AND FTHG < FTAG THEN 1
            WHEN AwayTeam = 'Lille' AND FTHG >= FTAG THEN 0
        END
    ) AS lille_wins_away,
FROM
    season
GROUP BY
    Div
