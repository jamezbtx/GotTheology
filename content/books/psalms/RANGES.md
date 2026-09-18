# Psalms ESV verse ranges

Paths: `content/books/psalms/<ch>/<start>-<end>.json` (hyphen in filenames; en-dash in display titles).
ESV / standard Protestant verse numbering (superscriptions not counted as verses).

**Total planned ranges: 171** (149 whole psalms + 22 stanzas for Psalm 119).

Do **not** invent commentary JSON here—specialists write each file using the same schema as Romans/Hebrews.

## Special rules

- **Default:** one range per psalm covering all verses (`psalms/<n>/1-<last>.json`).
- **Psalm 119:** split into the 22 alphabetic stanzas (8 verses each): 1-8, 9-16, … 169-176.
- **Long narrative / royal psalms:** keep whole unless a natural discourse split is unavoidable (prefer whole). Notably long wholes: 18 (50), 68 (35), 69 (36), 78 (72), 89 (52), 104 (35), 105 (45), 106 (48), 107 (43).
- **Psalm 117:** shortest (2 vv) — still its own file `psalms/117/1-2.json`.

## Editorial notes (for specialists)

- Psalms feed attributes-of-God hubs (holiness, mercy, faithfulness, sovereignty, etc.). Link passages to attribute hubs where natural; do not force.
- Do **not** cast genre / form-critical debates as Arminian vs Reformed.
- **Imprecatory psalms** (e.g. 35, 58, 69, 109, 137): both camps take them seriously; fair notes on both sides; no caricature.
- **Messianic readings:** shared christology where historic Arminian and Reformed camps agree; do **not** invent dispensational vs amillennial as the Arminian/Reformed fork.

## CANONICAL_BOOKS / build-site

- `scripts/build-site.js` already lists `{ name: "Psalms", slug: "psalms", testament: "ot" }` in `CANONICAL_BOOKS`.
- Build discovers passage JSON under `content/books/<slug>/`; empty chapter dirs with only `.gitkeep` produce no passage pages.
- Once JSON lands, book/chapter hubs and search index pick them up automatically. Homepage chrome / featured chips not required for this scaffold.

## Specialist blocks (7 agents; balanced)

Range counts aim ~22–25 files each; Psalm 119 is one dedicated block. Agent G has more *files* but mostly short Songs of Ascents; Agents D–E carry the heaviest single-file verse counts (78, 89, 104–107).

| Agent | Psalms | Ranges | Notes |
|------:|--------|-------:|-------|
| A | 1–25 | 25 | Book I start; wisdom / kingship (1–2, 8, 19, 22–24) |
| B | 26–50 | 25 | Book I end → Book II; lament clusters |
| C | 51–75 | 25 | Book II–III; penitential 51; Asaph start |
| D | 76–100 | 25 | Includes long narrative **78** (72vv) and royal **89** (52vv) |
| E | 101–118 | 18 | Book IV–V hinge; long **104–107**; Hallel 113–118 |
| F | **119** only | 22 | All 22 alphabetic stanzas (do not split across agents) |
| G | 120–150 | 31 | Songs of Ascents + finale; many short files |

**Optional 8th agent:** split G into G1 `120–135` (16 ranges) and G2 `136–150` (15 ranges) if load needs evening; keep F (119) intact.

## Planned full book (171 ranges)

### 1
_Psalm 1 (6 vv) — whole psalm_
- `psalms/1/1-6.json`

### 2
_Psalm 2 (12 vv) — whole psalm_
- `psalms/2/1-12.json`

### 3
_Psalm 3 (8 vv) — whole psalm_
- `psalms/3/1-8.json`

### 4
_Psalm 4 (8 vv) — whole psalm_
- `psalms/4/1-8.json`

### 5
_Psalm 5 (12 vv) — whole psalm_
- `psalms/5/1-12.json`

### 6
_Psalm 6 (10 vv) — whole psalm_
- `psalms/6/1-10.json`

### 7
_Psalm 7 (17 vv) — whole psalm_
- `psalms/7/1-17.json`

### 8
_Psalm 8 (9 vv) — whole psalm_
- `psalms/8/1-9.json`

### 9
_Psalm 9 (20 vv) — whole psalm_
- `psalms/9/1-20.json`

### 10
_Psalm 10 (18 vv) — whole psalm_
- `psalms/10/1-18.json`

### 11
_Psalm 11 (7 vv) — whole psalm_
- `psalms/11/1-7.json`

### 12
_Psalm 12 (8 vv) — whole psalm_
- `psalms/12/1-8.json`

### 13
_Psalm 13 (6 vv) — whole psalm_
- `psalms/13/1-6.json`

### 14
_Psalm 14 (7 vv) — whole psalm_
- `psalms/14/1-7.json`

### 15
_Psalm 15 (5 vv) — whole psalm_
- `psalms/15/1-5.json`

### 16
_Psalm 16 (11 vv) — whole psalm_
- `psalms/16/1-11.json`

### 17
_Psalm 17 (15 vv) — whole psalm_
- `psalms/17/1-15.json`

### 18
_Psalm 18 (50 vv) — whole psalm_
- `psalms/18/1-50.json` — Whole psalm (long; 50 vv — keep intact)

### 19
_Psalm 19 (14 vv) — whole psalm_
- `psalms/19/1-14.json`

### 20
_Psalm 20 (9 vv) — whole psalm_
- `psalms/20/1-9.json`

### 21
_Psalm 21 (13 vv) — whole psalm_
- `psalms/21/1-13.json`

### 22
_Psalm 22 (31 vv) — whole psalm_
- `psalms/22/1-31.json`

### 23
_Psalm 23 (6 vv) — whole psalm_
- `psalms/23/1-6.json`

### 24
_Psalm 24 (10 vv) — whole psalm_
- `psalms/24/1-10.json`

### 25
_Psalm 25 (22 vv) — whole psalm_
- `psalms/25/1-22.json`

### 26
_Psalm 26 (12 vv) — whole psalm_
- `psalms/26/1-12.json`

### 27
_Psalm 27 (14 vv) — whole psalm_
- `psalms/27/1-14.json`

### 28
_Psalm 28 (9 vv) — whole psalm_
- `psalms/28/1-9.json`

### 29
_Psalm 29 (11 vv) — whole psalm_
- `psalms/29/1-11.json`

### 30
_Psalm 30 (12 vv) — whole psalm_
- `psalms/30/1-12.json`

### 31
_Psalm 31 (24 vv) — whole psalm_
- `psalms/31/1-24.json`

### 32
_Psalm 32 (11 vv) — whole psalm_
- `psalms/32/1-11.json`

### 33
_Psalm 33 (22 vv) — whole psalm_
- `psalms/33/1-22.json`

### 34
_Psalm 34 (22 vv) — whole psalm_
- `psalms/34/1-22.json`

### 35
_Psalm 35 (28 vv) — whole psalm_
- `psalms/35/1-28.json`

### 36
_Psalm 36 (12 vv) — whole psalm_
- `psalms/36/1-12.json`

### 37
_Psalm 37 (40 vv) — whole psalm_
- `psalms/37/1-40.json` — Whole psalm (long; 40 vv — keep intact)

### 38
_Psalm 38 (22 vv) — whole psalm_
- `psalms/38/1-22.json`

### 39
_Psalm 39 (13 vv) — whole psalm_
- `psalms/39/1-13.json`

### 40
_Psalm 40 (17 vv) — whole psalm_
- `psalms/40/1-17.json`

### 41
_Psalm 41 (13 vv) — whole psalm_
- `psalms/41/1-13.json`

### 42
_Psalm 42 (11 vv) — whole psalm_
- `psalms/42/1-11.json`

### 43
_Psalm 43 (5 vv) — whole psalm_
- `psalms/43/1-5.json`

### 44
_Psalm 44 (26 vv) — whole psalm_
- `psalms/44/1-26.json`

### 45
_Psalm 45 (17 vv) — whole psalm_
- `psalms/45/1-17.json`

### 46
_Psalm 46 (11 vv) — whole psalm_
- `psalms/46/1-11.json`

### 47
_Psalm 47 (9 vv) — whole psalm_
- `psalms/47/1-9.json`

### 48
_Psalm 48 (14 vv) — whole psalm_
- `psalms/48/1-14.json`

### 49
_Psalm 49 (20 vv) — whole psalm_
- `psalms/49/1-20.json`

### 50
_Psalm 50 (23 vv) — whole psalm_
- `psalms/50/1-23.json`

### 51
_Psalm 51 (19 vv) — whole psalm_
- `psalms/51/1-19.json`

### 52
_Psalm 52 (9 vv) — whole psalm_
- `psalms/52/1-9.json`

### 53
_Psalm 53 (6 vv) — whole psalm_
- `psalms/53/1-6.json`

### 54
_Psalm 54 (7 vv) — whole psalm_
- `psalms/54/1-7.json`

### 55
_Psalm 55 (23 vv) — whole psalm_
- `psalms/55/1-23.json`

### 56
_Psalm 56 (13 vv) — whole psalm_
- `psalms/56/1-13.json`

### 57
_Psalm 57 (11 vv) — whole psalm_
- `psalms/57/1-11.json`

### 58
_Psalm 58 (11 vv) — whole psalm_
- `psalms/58/1-11.json`

### 59
_Psalm 59 (17 vv) — whole psalm_
- `psalms/59/1-17.json`

### 60
_Psalm 60 (12 vv) — whole psalm_
- `psalms/60/1-12.json`

### 61
_Psalm 61 (8 vv) — whole psalm_
- `psalms/61/1-8.json`

### 62
_Psalm 62 (12 vv) — whole psalm_
- `psalms/62/1-12.json`

### 63
_Psalm 63 (11 vv) — whole psalm_
- `psalms/63/1-11.json`

### 64
_Psalm 64 (10 vv) — whole psalm_
- `psalms/64/1-10.json`

### 65
_Psalm 65 (13 vv) — whole psalm_
- `psalms/65/1-13.json`

### 66
_Psalm 66 (20 vv) — whole psalm_
- `psalms/66/1-20.json`

### 67
_Psalm 67 (7 vv) — whole psalm_
- `psalms/67/1-7.json`

### 68
_Psalm 68 (35 vv) — whole psalm_
- `psalms/68/1-35.json`

### 69
_Psalm 69 (36 vv) — whole psalm_
- `psalms/69/1-36.json`

### 70
_Psalm 70 (5 vv) — whole psalm_
- `psalms/70/1-5.json`

### 71
_Psalm 71 (24 vv) — whole psalm_
- `psalms/71/1-24.json`

### 72
_Psalm 72 (20 vv) — whole psalm_
- `psalms/72/1-20.json`

### 73
_Psalm 73 (28 vv) — whole psalm_
- `psalms/73/1-28.json`

### 74
_Psalm 74 (23 vv) — whole psalm_
- `psalms/74/1-23.json`

### 75
_Psalm 75 (10 vv) — whole psalm_
- `psalms/75/1-10.json`

### 76
_Psalm 76 (12 vv) — whole psalm_
- `psalms/76/1-12.json`

### 77
_Psalm 77 (20 vv) — whole psalm_
- `psalms/77/1-20.json`

### 78
_Psalm 78 (72 vv) — whole psalm_
- `psalms/78/1-72.json` — Whole psalm (long; 72 vv — keep intact)

### 79
_Psalm 79 (13 vv) — whole psalm_
- `psalms/79/1-13.json`

### 80
_Psalm 80 (19 vv) — whole psalm_
- `psalms/80/1-19.json`

### 81
_Psalm 81 (16 vv) — whole psalm_
- `psalms/81/1-16.json`

### 82
_Psalm 82 (8 vv) — whole psalm_
- `psalms/82/1-8.json`

### 83
_Psalm 83 (18 vv) — whole psalm_
- `psalms/83/1-18.json`

### 84
_Psalm 84 (12 vv) — whole psalm_
- `psalms/84/1-12.json`

### 85
_Psalm 85 (13 vv) — whole psalm_
- `psalms/85/1-13.json`

### 86
_Psalm 86 (17 vv) — whole psalm_
- `psalms/86/1-17.json`

### 87
_Psalm 87 (7 vv) — whole psalm_
- `psalms/87/1-7.json`

### 88
_Psalm 88 (18 vv) — whole psalm_
- `psalms/88/1-18.json`

### 89
_Psalm 89 (52 vv) — whole psalm_
- `psalms/89/1-52.json` — Whole psalm (long; 52 vv — keep intact)

### 90
_Psalm 90 (17 vv) — whole psalm_
- `psalms/90/1-17.json`

### 91
_Psalm 91 (16 vv) — whole psalm_
- `psalms/91/1-16.json`

### 92
_Psalm 92 (15 vv) — whole psalm_
- `psalms/92/1-15.json`

### 93
_Psalm 93 (5 vv) — whole psalm_
- `psalms/93/1-5.json`

### 94
_Psalm 94 (23 vv) — whole psalm_
- `psalms/94/1-23.json`

### 95
_Psalm 95 (11 vv) — whole psalm_
- `psalms/95/1-11.json`

### 96
_Psalm 96 (13 vv) — whole psalm_
- `psalms/96/1-13.json`

### 97
_Psalm 97 (12 vv) — whole psalm_
- `psalms/97/1-12.json`

### 98
_Psalm 98 (9 vv) — whole psalm_
- `psalms/98/1-9.json`

### 99
_Psalm 99 (9 vv) — whole psalm_
- `psalms/99/1-9.json`

### 100
_Psalm 100 (5 vv) — whole psalm_
- `psalms/100/1-5.json`

### 101
_Psalm 101 (8 vv) — whole psalm_
- `psalms/101/1-8.json`

### 102
_Psalm 102 (28 vv) — whole psalm_
- `psalms/102/1-28.json`

### 103
_Psalm 103 (22 vv) — whole psalm_
- `psalms/103/1-22.json`

### 104
_Psalm 104 (35 vv) — whole psalm_
- `psalms/104/1-35.json`

### 105
_Psalm 105 (45 vv) — whole psalm_
- `psalms/105/1-45.json` — Whole psalm (long; 45 vv — keep intact)

### 106
_Psalm 106 (48 vv) — whole psalm_
- `psalms/106/1-48.json` — Whole psalm (long; 48 vv — keep intact)

### 107
_Psalm 107 (43 vv) — whole psalm_
- `psalms/107/1-43.json` — Whole psalm (long; 43 vv — keep intact)

### 108
_Psalm 108 (13 vv) — whole psalm_
- `psalms/108/1-13.json`

### 109
_Psalm 109 (31 vv) — whole psalm_
- `psalms/109/1-31.json`

### 110
_Psalm 110 (7 vv) — whole psalm_
- `psalms/110/1-7.json`

### 111
_Psalm 111 (10 vv) — whole psalm_
- `psalms/111/1-10.json`

### 112
_Psalm 112 (10 vv) — whole psalm_
- `psalms/112/1-10.json`

### 113
_Psalm 113 (9 vv) — whole psalm_
- `psalms/113/1-9.json`

### 114
_Psalm 114 (8 vv) — whole psalm_
- `psalms/114/1-8.json`

### 115
_Psalm 115 (18 vv) — whole psalm_
- `psalms/115/1-18.json`

### 116
_Psalm 116 (19 vv) — whole psalm_
- `psalms/116/1-19.json`

### 117
_Psalm 117 (2 vv) — whole psalm_
- `psalms/117/1-2.json`

### 118
_Psalm 118 (29 vv) — whole psalm_
- `psalms/118/1-29.json`

### 119
_Psalm 119 (176 vv) — 22 alphabetic stanzas_
- `psalms/119/1-8.json` — Alphabetic stanza 1/22 (Aleph)
- `psalms/119/9-16.json` — Alphabetic stanza 2/22 (Beth)
- `psalms/119/17-24.json` — Alphabetic stanza 3/22 (Gimel)
- `psalms/119/25-32.json` — Alphabetic stanza 4/22 (Daleth)
- `psalms/119/33-40.json` — Alphabetic stanza 5/22 (He)
- `psalms/119/41-48.json` — Alphabetic stanza 6/22 (Waw)
- `psalms/119/49-56.json` — Alphabetic stanza 7/22 (Zayin)
- `psalms/119/57-64.json` — Alphabetic stanza 8/22 (Heth)
- `psalms/119/65-72.json` — Alphabetic stanza 9/22 (Teth)
- `psalms/119/73-80.json` — Alphabetic stanza 10/22 (Yodh)
- `psalms/119/81-88.json` — Alphabetic stanza 11/22 (Kaph)
- `psalms/119/89-96.json` — Alphabetic stanza 12/22 (Lamedh)
- `psalms/119/97-104.json` — Alphabetic stanza 13/22 (Mem)
- `psalms/119/105-112.json` — Alphabetic stanza 14/22 (Nun)
- `psalms/119/113-120.json` — Alphabetic stanza 15/22 (Samekh)
- `psalms/119/121-128.json` — Alphabetic stanza 16/22 (Ayin)
- `psalms/119/129-136.json` — Alphabetic stanza 17/22 (Pe)
- `psalms/119/137-144.json` — Alphabetic stanza 18/22 (Tsadhe)
- `psalms/119/145-152.json` — Alphabetic stanza 19/22 (Qoph)
- `psalms/119/153-160.json` — Alphabetic stanza 20/22 (Resh)
- `psalms/119/161-168.json` — Alphabetic stanza 21/22 (Sin and Shin)
- `psalms/119/169-176.json` — Alphabetic stanza 22/22 (Taw)

### 120
_Psalm 120 (7 vv) — whole psalm_
- `psalms/120/1-7.json`

### 121
_Psalm 121 (8 vv) — whole psalm_
- `psalms/121/1-8.json`

### 122
_Psalm 122 (9 vv) — whole psalm_
- `psalms/122/1-9.json`

### 123
_Psalm 123 (4 vv) — whole psalm_
- `psalms/123/1-4.json`

### 124
_Psalm 124 (8 vv) — whole psalm_
- `psalms/124/1-8.json`

### 125
_Psalm 125 (5 vv) — whole psalm_
- `psalms/125/1-5.json`

### 126
_Psalm 126 (6 vv) — whole psalm_
- `psalms/126/1-6.json`

### 127
_Psalm 127 (5 vv) — whole psalm_
- `psalms/127/1-5.json`

### 128
_Psalm 128 (6 vv) — whole psalm_
- `psalms/128/1-6.json`

### 129
_Psalm 129 (8 vv) — whole psalm_
- `psalms/129/1-8.json`

### 130
_Psalm 130 (8 vv) — whole psalm_
- `psalms/130/1-8.json`

### 131
_Psalm 131 (3 vv) — whole psalm_
- `psalms/131/1-3.json`

### 132
_Psalm 132 (18 vv) — whole psalm_
- `psalms/132/1-18.json`

### 133
_Psalm 133 (3 vv) — whole psalm_
- `psalms/133/1-3.json`

### 134
_Psalm 134 (3 vv) — whole psalm_
- `psalms/134/1-3.json`

### 135
_Psalm 135 (21 vv) — whole psalm_
- `psalms/135/1-21.json`

### 136
_Psalm 136 (26 vv) — whole psalm_
- `psalms/136/1-26.json`

### 137
_Psalm 137 (9 vv) — whole psalm_
- `psalms/137/1-9.json`

### 138
_Psalm 138 (8 vv) — whole psalm_
- `psalms/138/1-8.json`

### 139
_Psalm 139 (24 vv) — whole psalm_
- `psalms/139/1-24.json`

### 140
_Psalm 140 (13 vv) — whole psalm_
- `psalms/140/1-13.json`

### 141
_Psalm 141 (10 vv) — whole psalm_
- `psalms/141/1-10.json`

### 142
_Psalm 142 (7 vv) — whole psalm_
- `psalms/142/1-7.json`

### 143
_Psalm 143 (12 vv) — whole psalm_
- `psalms/143/1-12.json`

### 144
_Psalm 144 (15 vv) — whole psalm_
- `psalms/144/1-15.json`

### 145
_Psalm 145 (21 vv) — whole psalm_
- `psalms/145/1-21.json`

### 146
_Psalm 146 (10 vv) — whole psalm_
- `psalms/146/1-10.json`

### 147
_Psalm 147 (20 vv) — whole psalm_
- `psalms/147/1-20.json`

### 148
_Psalm 148 (14 vv) — whole psalm_
- `psalms/148/1-14.json`

### 149
_Psalm 149 (9 vv) — whole psalm_
- `psalms/149/1-9.json`

### 150
_Psalm 150 (6 vv) — whole psalm_
- `psalms/150/1-6.json`

## Units kept intact (do not split)

Every psalm except 119 is one unit. Within 119, each 8-verse alphabetic stanza is one unit (do not merge stanzas; do not split mid-stanza).

Local only: no git commit, no push, no publish until Theology Bot congruence / assignment.
