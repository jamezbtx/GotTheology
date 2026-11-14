import re
head=open('/tmp/head.html').read(); foot=open('/tmp/foot.html').read()
def page(title, desc, path, body, footer_label):
    h=head.replace('<title>Articles — GotTheology</title>', f'<title>{title} — GotTheology</title>')
    h=re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>'+desc, h)
    h=re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>'+desc, h)
    h=h.replace('content="Articles — GotTheology"', f'content="{title} — GotTheology"')
    h=h.replace('https://got-theology.com/articles/', 'https://got-theology.com'+path)
    h=h.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0" />','<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n  <meta name="robots" content="noindex,nofollow" />')
    h=h.replace('<link rel="stylesheet" href="/assets/gottheology.css" />','<link rel="stylesheet" href="/assets/gottheology.css" />\n  <link rel="stylesheet" href="/assets/creeds.css" />')
    h=h.replace('        <a href="/articles/">Articles</a>\n','        <a href="/articles/">Articles</a>\n        <a href="/creeds/">Creeds</a>\n',1)
    f=foot.replace('          <a href="/articles/">Articles</a>\n','          <a href="/articles/">Articles</a>\n          <a href="/creeds/">Creeds</a>\n',1)
    f=f.replace('<span>Articles</span>', f'<span>{footer_label}</span>')
    return h+body+f

def chip(label, href):
    return f'<a class="topic-chip creed-ref" href="{href}">{label}</a>'

sections=[
 ("God the Father",
  "I Believe in one God the Father Almighty, Maker of heaven and earth, And of all things visible and invisible.",
  [("Genesis 1:1","/bible/genesis/1/1-5#v1"),("Colossians 1:16","/bible/colossians/1/15-23#v16")]),
 ("The eternal Son",
  "And in one Lord Jesus Christ, the only begotten Son of God, Begotten of his Father before all worlds, God of God, Light of Light, Very God of very God, Begotten, not made, Being of one substance with the Father, By whom all things were made:",
  [("John 1:1–3","/bible/john/1/1-18#v1"),("John 1:14","/bible/john/1/1-18#v14"),("John 3:16","/bible/john/3/1-21#v16"),("Hebrews 1:2–3","/bible/hebrews/1/1-4#v2"),("Philippians 2:6","/bible/philippians/2/1-11#v6")]),
 ("The incarnate Son",
  "Who for us men, and for our salvation came down from heaven, And was incarnate by the Holy Ghost of the Virgin Mary, And was made man,",
  [("John 6:38","/bible/john/6/22-40#v38"),("Matthew 1:20","/bible/matthew/1/18-25#v20"),("Luke 1:35","/bible/luke/1/26-38#v35"),("John 1:14","/bible/john/1/1-18#v14")]),
 ("Crucified, risen, ascended",
  "And was crucified also for us under Pontius Pilate: He suffered and was buried, And the third day he rose again according to the Scriptures, And ascended into heaven, And sitteth on the right hand of the Father:",
  [("Matthew 27:2","/bible/matthew/27/1-2#v2"),("1 Corinthians 15:3–4","/bible/1-corinthians/15/1-11#v3"),("Acts 1:9","/bible/acts/1/1-11#v9"),("Hebrews 1:3","/bible/hebrews/1/1-4#v3")]),
 ("The coming King",
  "And he shall come again with glory to judge both the quick and the dead; Whose kingdom shall have no end.",
  [("Matthew 25:31","/bible/matthew/25/31-46#v31"),("Acts 10:42","/bible/acts/10/24-48#v42"),("2 Timothy 4:1","/bible/2-timothy/4/1-8#v1"),("Luke 1:33","/bible/luke/1/26-38#v33"),("Daniel 7:14","/bible/daniel/7/1-14#v14")]),
 ("The Holy Spirit",
  "And I believe in the Holy Ghost, The Lord and giver of life, Who proceedeth from the Father <mark class=\"filioque\">and the Son</mark>, Who with the Father and the Son together is worshipped and glorified, Who spake by the Prophets.",
  [("2 Corinthians 3:17","/bible/2-corinthians/3/12-18#v17"),("John 6:63","/bible/john/6/60-71#v63"),("John 15:26","/bible/john/15/18-27#v26"),("John 16:7","/bible/john/16/1-15#v7"),("2 Peter 1:21","/bible/2-peter/1/12-21#v21")]),
 ("The church and the life to come",
  "And I believe one Catholick and Apostolick Church. I acknowledge one Baptism for the remission of sins. And I look for the Resurrection of the dead, And the Life of the world to come. Amen.",
  [("Ephesians 4:4–5","/bible/ephesians/4/1-16#v4"),("Ephesians 2:20","/bible/ephesians/2/11-22#v20"),("Acts 2:38","/bible/acts/2/37-47#v38"),("John 5:28–29","/bible/john/5/19-29#v28"),("1 Corinthians 15:52","/bible/1-corinthians/15/50-58#v52"),("Revelation 21:4","/bible/revelation/21/1-8#v4")]),
]
cards=[]
for i,(label,text,refs) in enumerate(sections,1):
    extra=''
    if label=="The Holy Spirit":
        extra='''
        <aside class="creed-note" role="note"><strong>“And the Son.”</strong> These words (Latin <em>filioque</em>) were not in the creed as received at Chalcedon in 451, which says the Spirit proceeds “from the Father.” Western churches added them gradually from the sixth century; the Third Council of Toledo (589, as traditionally dated) is the earliest commonly cited use, and the creed was sung with the addition at Mass in Rome from about 1014. Roman Catholic, Anglican and most Protestant churches kept the addition, as the Prayer Book text does. The Eastern Orthodox churches confess the creed without it and regard the addition as unauthorized.</aside>'''
    if label=="The church and the life to come":
        extra='''
        <aside class="creed-note" role="note"><strong>“Catholick.”</strong> The word means “universal,” the whole church in every place, not one denomination. The Prayer Book line omits “holy,” which the Greek text has (“one holy catholic and apostolic church”); the omission goes back to Cranmer’s 1549 English text, and many later Anglican books restored the word.</aside>'''
    chips=''.join('\n            '+chip(l,h) for l,h in refs)
    cards.append(f'''
      <article class="verse-card creed-card" id="part{i}">
        <div class="verse-text-block">
          <p class="verse-ref">{label}</p>
          <p class="verse-scripture creed-text">{text}</p>
        </div>
        <div class="creed-refs">
          <span class="topic-chips-label">Scripture</span>
          <div class="topic-chips-row">{chips}
          </div>
        </div>{extra}
      </article>''')

body=f'''  <main class="bible-index article-page creed-page">
    <div class="reader article">
      <p class="browse-crumbs"><a href="/">Home</a> <span aria-hidden="true">›</span> <a href="/creeds/">Creeds &amp; Confessions</a></p>
      <div class="page-intro">
        <p class="eyebrow">Ecumenical Creed</p>
        <h1>The Nicene Creed</h1>
        <p>The Niceno-Constantinopolitan Creed: Nicaea, 325, and Constantinople, 381. Confessed by Arminian and Reformed churches alike.</p>
        <div class="passage-meta creed-meta">
          <span>Council of Constantinople, 381</span>
          <span aria-hidden="true">·</span>
          <span>Text: Book of Common Prayer, 1662</span>
          <span class="pill">Public domain</span>
        </div>
      </div>

      <h2>Background</h2>
      <p>In 325 the Emperor Constantine called the Council of Nicaea to settle the dispute over Arius, who taught that the Son was a created being. The council issued a creed confessing the Son to be “of one substance” (Greek <em>homoousios</em>) with the Father. The longer creed printed here, with its fuller article on the Holy Spirit, has long been credited to the Council of Constantinople in 381. That council’s own records are lost, and the earliest explicit statement that the text came from it is at the Council of Chalcedon in 451, where it was read as the faith of the 150 fathers of Constantinople. Scholars still debate how it was composed; many think it drew on an existing baptismal creed rather than simply enlarging the creed of 325. It is the one creed accepted as authoritative by the Roman Catholic, Eastern Orthodox, Anglican and major Protestant churches.</p>

      <h2>The text</h2>
      <p class="creed-version">From the Communion service of the <em>Book of Common Prayer</em> (1662), the traditional English form used for centuries in Anglican worship. Spelling follows the 1762 Baskerville printing, with the old long “s” modernized. Scripture links open our verse-by-verse commentary.</p>
      <div class="verse-list creed-list">{''.join(cards)}
      </div>

      <h2>Where both traditions stand</h2>
      <p>There is no Arminian–Reformed divide here. The creed confesses the Trinity and the person and work of Christ, and it does not take up the questions of election and grace on which the two traditions differ. Both read its words the same way.</p>
      <div class="dual-cols creed-dual">
        <div class="dual-col">
          <span class="dual-label label-arminian">Arminian</span>
          <p>John Wesley was an Anglican priest, and the Church of England’s Article 8 says the Nicene, Athanasian and Apostles’ creeds “ought thoroughly to be received and believed.” When he abridged the Articles for American Methodists in 1784, Wesley left Article 8 out, and his <em>Sunday Service</em> dropped the Nicene Creed from the Lord’s Supper while keeping the Apostles’ Creed. He gave no reason, and Methodist scholars generally hold that he did not reject the creed’s teaching. The Nicene Creed is printed in the <em>United Methodist Hymnal</em> today.</p>
        </div>
        <div class="dual-col">
          <span class="dual-label label-reformed">Reformed</span>
          <p>The Belgic Confession (1561), one of the doctrinal standards of the Dutch Reformed churches, ends its article on the Trinity (Article 9) by receiving “the three ecumenical creeds—the Apostles’, Nicene, and Athanasian.” Reformed Anglicans receive it through Article 8 of the Thirty-Nine Articles. The Belgic Confession’s Article 7 sets no human writing or council above the truth of God in Scripture, so the creed is received as a faithful summary of Scripture, not an addition to it.</p>
        </div>
      </div>

      <h2>Sources</h2>
      <ul class="creed-sources">
        <li><em>Book of Common Prayer</em> (1662), Holy Communion; Baskerville printing of 1762, transcribed at justus.anglican.org.</li>
        <li><em>Articles of Religion</em> (1562/1571), Article 8, “Of the Three Creeds,” in the same printing.</li>
        <li>Belgic Confession, Article 9 (Christian Reformed Church in North America translation).</li>
        <li>“Nicene Creed,” <em>Encyclopaedia Britannica</em>: composition and the filioque.</li>
        <li>North American Orthodox–Catholic Theological Consultation, <em>The Filioque: A Church-Dividing Issue?</em> (2003).</li>
        <li>“Why do we say creeds?” United Methodist Communications (umc.org): Wesley’s omissions in 1784.</li>
      </ul>

      <aside class="disclaimer" role="note"><strong>About these notes.</strong>
        Historical notes are educational and cite their sources. Where scholars disagree, we say so. Commentary links open our verse-by-verse pages, where Arminian and Reformed readings sit side by side.</aside>
    </div>
  </main>
'''
open('/workspace/gt-creeds-mock/public/creeds/nicene-creed.html','w').write(page('The Nicene Creed (381)','The Niceno-Constantinopolitan Creed in the 1662 Book of Common Prayer text, with background, the filioque, Scripture links, and where Arminian and Reformed churches stand.','/creeds/nicene-creed',body,'Creeds &amp; Confessions'))

idx='''  <main class="bible-index articles-hub creeds-hub">
    <div class="reader">
      <p class="browse-crumbs"><a href="/">Home</a></p>
      <div class="page-intro page-intro--hub">
        <p class="eyebrow">Historical</p>
        <h1>Creeds &amp; Confessions</h1>
        <p>The creeds the whole church confesses, and the confessions behind the Arminian and Reformed traditions, with background and links to the Scriptures they cite.</p>
      </div>
      <ul class="passage-list">
        <li><a href="/creeds/nicene-creed"><span class="ref">The Nicene Creed (381)</span><span class="meta">The Niceno-Constantinopolitan Creed in the 1662 Prayer Book text, with Scripture links and where both traditions stand.</span></a></li>
      </ul>
    </div>
  </main>
'''
open('/workspace/gt-creeds-mock/public/creeds/index.html','w').write(page('Creeds &amp; Confessions','Historic Christian creeds and Arminian and Reformed confessions, with background and Scripture links.','/creeds/',idx,'Creeds &amp; Confessions'))
