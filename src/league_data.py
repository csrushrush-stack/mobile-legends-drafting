# -*- coding: utf-8 -*-
"""League hero-stat tables for the draft app.

Every row is (hero, picks, wins, losses, bans).
Win/loss derived from the published win rate where the source gave a percentage.
'games' is the tournament game count, verified against the published ban% where possible.
"""

# ---- Asian Games 2026 (Aichi-Nagoya) - 32 games, 15 tracked heroes -------------
AG2026 = dict(id="ag", name="Asian Games 2026", short="AG26", region="International",
              games=32, note="MLBB's debut as an official medal event. Gold: Myanmar.",
              rows=[("Nolan",23,11,12,6),("Hirara",16,12,4,15),("Aulus",16,11,5,16),
                    ("Eudora",16,10,6,7),("Obsidia",15,9,6,6),("Esmeralda",14,7,7,8),
                    ("Atlas",13,8,5,19),("Minotaur",13,8,5,13),("Uranus",13,5,8,12),
                    ("Zhuxin",12,6,6,3),("Gloo",11,7,4,6),("Paquito",11,5,6,13),
                    ("Carmilla",11,3,8,19),("Belerick",9,2,7,4),("Valentina",6,6,0,6)])

# ---- MPL Philippines S18 - 166 games ---------------------------------------
PH18 = dict(id="ph", name="MPL Philippines S18", short="PH", region="Philippines",
            games=166, note="Current MPL PH season. Hirara is the most-picked hero in the league.",
            rows=[("Hirara",122,55,67,38),("Paquito",70,42,28,76),("Belerick",67,36,31,25),
                  ("Eudora",63,32,31,30),("Nolan",62,36,26,34),("Minotaur",56,26,30,20),
                  ("Gatotkaca",54,22,32,12),("Barats",51,29,22,58),("Carmilla",49,22,27,44),
                  ("Aulus",47,26,21,30),("Valentina",46,21,25,34),("Marcel",44,25,19,73),
                  ("Uranus",42,21,21,72),("Claude",41,25,16,8),("Zhuxin",39,22,17,33),
                  ("Obsidia",37,19,18,24),("Selena",36,17,19,63),("Clint",31,22,9,11),
                  ("Atlas",30,19,11,132),("Cici",29,12,17,12),("Hylos",29,14,15,5),
                  ("Rafaela",28,19,9,44),("Brody",28,7,21,21),("Esmeralda",27,10,17,52),
                  ("Kalea",26,10,16,18),("Suyou",26,14,12,5),("Mathilda",25,12,13,37),
                  ("Freya",24,18,6,142),("Alice",24,10,14,24),("Kimmy",24,12,12,16),
                  ("Melissa",23,10,13,52),("Gloo",22,13,9,36),("Novaria",21,10,11,11),
                  ("Miya",21,8,13,8),("Moskov",20,7,13,10),("Lylia",19,8,11,33),
                  ("Fanny",15,7,8,96),("Harley",13,4,9,17),("Masha",12,8,4,69),("Ruby",12,7,5,11),
                  ("Chou",12,4,8,6),("Vexana",12,7,5,4),("Lukas",11,5,6,10),("Badang",10,3,7,12),
                  ("Angela",10,4,6,10),("Phoveus",10,3,7,3),("Bruno",10,3,7,2),("Yve",9,6,3,4),
                  ("Zetian",9,4,5,3),("Yi Sun-shin",9,3,6,3),("Pharsa",9,7,2,2),
                  ("Cecilion",8,1,7,5),("Harith",7,4,3,4),("Sora",7,3,4,4),("Kaja",6,4,2,11),
                  ("Dyrroth",6,3,3,8),("Karrie",6,3,3,0),("Hanabi",4,3,1,8),("Hilda",4,3,1,5),
                  ("Arlott",4,2,2,4),("Beatrix",4,3,1,2),("Hayabusa",4,1,3,2),("Khufra",4,3,1,1),
                  ("Aurora",3,2,1,3),("Khaleed",3,1,2,1),("Lapu-Lapu",3,2,1,0),
                  ("Yu Zhong",3,2,1,0),("Luo Yi",3,1,2,0),("Saber",1,0,1,2),("Estes",1,1,0,1),
                  ("Fredrinn",1,0,1,1),("Hanzo",1,0,1,1),("Edith",1,1,0,0),("Lunox",1,1,0,0),
                  ("Baxia",1,0,1,0),("Granger",1,0,1,0),("Guinevere",1,0,1,0),("Kagura",1,0,1,0),
                  ("Leomord",1,0,1,0),("Ling",1,0,1,0),("Lolita",1,0,1,0),("Thamuz",1,0,1,0),
                  ("Xavier",1,0,1,0)])

# ---- MPL Indonesia S18 - 174 games -----------------------------------------
ID18 = dict(id="id", name="MPL Indonesia S18", short="ID", region="Indonesia",
            games=174, note="Current MPL ID season, and the deepest hero pool of the three.",
            rows=[("Paquito",87,39,48,58),("Hirara",84,45,39,80),("Belerick",68,34,34,20),
                  ("Claude",60,31,29,10),("Nolan",54,32,22,46),("Aulus",51,29,22,19),
                  ("Uranus",49,23,26,53),("Eudora",49,27,22,30),("Selena",46,19,27,48),
                  ("Zhuxin",46,23,23,43),("Atlas",43,24,19,120),("Obsidia",43,27,16,28),
                  ("Minotaur",43,18,25,28),("Freya",42,22,20,129),("Valentina",42,15,27,24),
                  ("Cici",40,21,19,17),("Carmilla",39,22,17,64),("Barats",39,18,21,43),
                  ("Rafaela",37,20,17,44),("Gloo",37,21,16,41),("Alice",35,19,16,19),
                  ("Melissa",34,18,16,53),("Kimmy",33,18,15,11),("Moskov",32,17,15,14),
                  ("Esmeralda",30,13,17,55),("Marcel",29,19,10,84),("Brody",28,8,20,13),
                  ("Lylia",27,13,14,27),("Miya",27,17,10,18),("Gatotkaca",27,16,11,11),
                  ("Mathilda",22,11,11,51),("Fanny",21,11,10,105),("Novaria",20,10,10,38),
                  ("Hylos",20,9,11,3),("Lukas",19,11,8,28),("Zetian",19,14,5,14),
                  ("Harley",18,6,12,12),("Badang",17,9,8,7),("Sora",17,7,10,7),("Alpha",16,9,7,5),
                  ("Phoveus",15,8,7,19),("Cecilion",15,10,5,7),("Suyou",15,5,10,1),
                  ("Yi Sun-shin",14,5,9,11),("Ruby",14,7,7,8),("Chou",14,4,10,7),
                  ("Masha",13,4,9,61),("Kalea",13,7,6,7),("Arlott",11,5,6,25),("Dyrroth",9,5,4,3),
                  ("Chip",7,1,6,22),("Clint",7,3,4,0),("Saber",6,4,2,4),("Hayabusa",6,2,4,3),
                  ("Yve",6,4,2,0),("Terizla",6,3,3,0),("Pharsa",6,2,4,0),("Lunox",5,1,4,2),
                  ("Hanabi",4,2,2,3),("Hanzo",4,2,2,3),("Leomord",4,2,2,1),("Kaja",3,1,2,10),
                  ("Guinevere",3,2,1,6),("Angela",3,0,3,3),("Fredrinn",3,1,2,2),("Bruno",3,2,1,1),
                  ("Hilda",3,3,0,0),("Valir",3,2,1,0),("Vexana",2,1,1,5),("Estes",2,1,1,1),
                  ("Wanwan",2,1,1,1),("Faramis",2,1,1,0),("Khaleed",2,1,1,0),("Argus",2,0,2,0),
                  ("Harith",2,0,2,0),("Joy",2,0,2,0),("Kadita",2,0,2,0),("Karrie",2,0,2,0),
                  ("Khufra",2,0,2,0),("Odette",2,0,2,0),("Ling",1,0,1,1),("Ixia",1,1,0,0),
                  ("Kagura",1,1,0,0),("Lapu-Lapu",1,1,0,0),("Edith",1,0,1,0),("Granger",1,0,1,0),
                  ("Lesley",1,0,1,0),("Luo Yi",1,0,1,0),("Minsitthar",1,0,1,0),
                  ("Tigreal",1,0,1,0),("Yu Zhong",1,0,1,0)])

# ---- MSL Myanmar S4 - 119 games --------------------------------------------
MM4 = dict(id="mm", name="MSL Myanmar S4", short="MM", region="Myanmar",
            games=119, note="Myanmar won Asian Games gold off the back of this league.",
            rows=[("Hirara",81,39,42,35),("Paquito",65,36,29,22),("Belerick",62,32,30,40),
                  ("Eudora",62,35,27,18),("Uranus",47,24,23,57),("Gloo",38,23,15,32),
                  ("Zhuxin",36,17,19,36),("Nolan",35,20,15,11),("Obsidia",32,13,19,16),
                  ("Barats",31,12,19,27),("Minotaur",31,18,13,22),("Esmeralda",28,12,16,27),
                  ("Carmilla",27,11,16,37),("Rafaela",27,13,14,24),("Brody",26,19,7,32),
                  ("Freya",24,16,8,94),("Gatotkaca",24,12,12,9),("Miya",24,12,12,7),
                  ("Selena",22,11,11,31),("Melissa",21,13,8,44),("Dyrroth",19,11,8,12),
                  ("Moskov",18,5,13,18),("Alice",18,9,9,14),("Zetian",18,8,10,1),
                  ("Aulus",17,7,10,18),("Yi Sun-shin",17,8,9,14),("Novaria",17,8,9,7),
                  ("Kimmy",15,8,7,6),("Chou",15,4,11,5),("Atlas",14,6,8,97),("Clint",14,7,7,3),
                  ("Ruby",13,5,8,8),("Sora",13,6,7,6),("Claude",13,7,6,5),("Granger",13,7,6,3),
                  ("Marcel",12,5,7,93),("Fanny",12,7,5,40),("Masha",12,7,5,23),("Cici",11,4,7,11),
                  ("Hylos",11,4,7,3),("Lylia",10,6,4,14),("Suyou",10,3,7,8),
                  ("Valentina",9,5,4,30),("Kalea",9,5,4,10),("Phoveus",9,4,5,9),("Bruno",9,5,4,4),
                  ("Mathilda",8,5,3,13),("Lukas",8,4,4,3),("Kaja",7,3,4,11),("Vexana",7,1,6,2),
                  ("Leomord",6,2,4,3),("Arlott",6,5,1,2),("Cecilion",5,2,3,3),("Harley",4,3,1,10),
                  ("Guinevere",4,3,1,4),("Angela",4,1,3,3),("Aurora",4,2,2,0),("Valir",3,3,0,2),
                  ("Khaleed",3,2,1,2),("Hanabi",3,0,3,2),("Harith",3,1,2,1),("Gord",3,2,1,0),
                  ("Tigreal",2,0,2,1),("Yu Zhong",2,1,1,0),("Beatrix",2,0,2,0),("Chip",1,1,0,12),
                  ("Badang",1,1,0,3),("Ixia",1,1,0,2),("Odette",1,0,1,2),("Kagura",1,0,1,1),
                  ("Lunox",1,0,1,1),("Faramis",1,1,0,0),("Jawhead",1,1,0,0),("Yve",1,1,0,0),
                  ("Argus",1,0,1,0),("Balmond",1,0,1,0),("Edith",1,0,1,0),("Karrie",1,0,1,0),
                  ("Pharsa",1,0,1,0),("Wanwan",1,0,1,0)])

LEAGUES = [AG2026, PH18, ID18, MM4]
