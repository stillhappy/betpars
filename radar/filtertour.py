filterteam = {'Berlin International': 'Big', 'Elevate^': 'Elevate', 'Barça': 'Barca', 'Five Media': 'Five Media Clan', 'Grp': 'Grypciocraft',
              'Hle': 'Hanwha Life', 'Vitality Bee': 'Vitality.Bee', '1W Academy': '1Win Academy', '9 Pandas': '9Pandas',
              'Aurora Yb': 'Aurora Young Blud', 'Austrian Force Willhaben': 'Austrian Force', 'Dynasty Ne': 'Dynasty', 'Faze': 'Faze Clan', 'Gng Amazigh': 'Gng',
              'Kabum Academy': 'Kabum! Academy', 'Los Grandes Academy': 'Los Academy', 'Mad Lions': 'Mad Lions Koi', 'Nigma Galaxy Mena': 'Nigma Galaxy',
              'Nip': 'Ninjas In Pyjamas', 'orangegaming': 'Orangegaming', 'West Point Philippines': 'West Point', 'Burning Core Toyama': 'Burning Core',
              'Breiðablik': 'Breidablik', 'Breioablik': 'Breidablik', 'Aoe': 'Area Of Effect', 'Dplus': 'Dplus Kia', 'Kabum': 'Kabum!'}

filtertourn = {'Arabian League Spring': 'Arabian League', 'BetBoom Dacha Dubai': 'BB Dacha', 'Campeonato Brasileiro (CBLoL)': 'Campeonato Brasileiro',
              'Turkish Championship League Winter': 'Turkish Championship League', 'Northern League of Legends Championship Spring': 'Northern LoL Championship',
              'Pacific Championship Series (PCS)': 'Pacific Championship Series', 'Elite Series: Spring': 'Elite Series', 'EPL': 'EPL World Series: Americas',
               'EPL World Series America': 'EPL World Series: Americas', 'EPL World Series: Americas Season 6': 'EPL World Series: Americas',
               'ESEA SEASON 48: ADVANCED DIVISION - EUROPE': 'ESEA Advanced Europe', 'ESL Challenger NA': 'ESL Challenger League North America', 'ESL Challenger SA': 'ESL Challenger League South America',
               'Esport Balkan League Spring': 'Esport Balkan League', 'La Ligue Française (LFL)': 'LFL', 'LCK Challengers League': 'LCK', 'LCK CL': 'LCK',
               'Liga Latinoamérica (LLA)': 'LLA', 'Liga Latinoamerica': 'LLA', 'PGL Major Copenhagen Europe': 'PGL Major Copenhagen',
               'PGL Major Copenhagen Europe RMR A': 'PGL Major Copenhagen', 'PGL Major Copenhagen Europe RMR B': 'PGL Major Copenhagen',
               'Prime League 1st Division': 'Prime League', 'Turkish Championship League': 'Turkish Champions League', 'Ultraliga Season 11': 'Ultraliga',
               'TCL': 'Tencent LoL Pro League', 'LVP Super Liga': 'LVP Superliga', 'LVP SL': 'LVP Superliga'}

""" 
/////////ЗАПРОС В SQL НА ВСЕ УНИКАЛЬНЫЕ НАЗВАНИЯ КОМАНД + БК
SELECT team, bk_name
FROM (
    SELECT team1 AS team, bk_name
    FROM datakofs
    UNION
    SELECT team2 AS team, bk_name
    FROM datakofs
) AS subquery
ORDER BY team;

/////////ЗАПРОС В SQL НА ИЗМЕНЕНИЕ НАЗВАНИЯ ТУРНИРА ПО ФОНБЕТУ
UPDATE datakofs
SET tour_name = (
    SELECT COALESCE(
        (
            SELECT t2.tour_name
    FROM datakofs AS t2
    WHERE t2.bk_name = 'Fonbet' AND (t2.team1 = datakofs.team1 AND t2.team2 = datakofs.team2 OR t2.team1 = datakofs.team2 AND t2.team2 = datakofs.team1)
        AND t2.date_match BETWEEN (datakofs.date_match - INTERVAL '1 hour') AND (datakofs.date_match + INTERVAL '1 hour')
    LIMIT 1
        ),
        tour_name
    )
)
WHERE bk_name <> 'Fonbet';
"""