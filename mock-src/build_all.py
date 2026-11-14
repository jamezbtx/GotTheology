import pages_creeds as C, pages_reformed as RF, pages_arminian as A
from frame import page, OUT
order={}
for f in (C.apostles,C.athanasian,C.chalcedon,RF.heidelberg,RF.belgic,RF.dort,RF.wcf,RF.lbcf,A.remonstrance,A.remconf,A.wesley,A.fwb):
    order[f.__name__]=f()
G=[('ecumenical','Ecumenical creeds','Confessed by Arminian and Reformed churches alike, and by most other Christian churches.',[
  ('apostles-creed','The Apostles’ Creed','The baptismal creed of the Western church, in the 1662 Prayer Book text.'),
  ('nicene-creed','The Nicene Creed (381)','The creed of Nicaea and Constantinople, with a note on the filioque.'),
  ('chalcedonian-definition','The Chalcedonian Definition (451)','The council’s confession of Christ as one person in two natures.'),
  ('athanasian-creed','The Athanasian Creed','A Latin confession of the Trinity and the Incarnation, received by the Reformation churches.')]),
 ('reformed','Reformed confessions','The doctrinal standards of the Reformed, Presbyterian and Reformed Baptist churches.',[
  ('heidelberg-catechism','The Heidelberg Catechism (1563)','129 questions on comfort in Christ: sin and misery, redemption, and thankfulness.'),
  ('belgic-confession','The Belgic Confession (1561)','Guido de Brès’s thirty-seven articles for the Reformed churches of the Low Countries.'),
  ('canons-of-dort','The Canons of Dort (1619)','The Synod of Dort’s answer to the Remonstrance, under five heads of doctrine.'),
  ('westminster-confession','The Westminster Confession of Faith (1646)','The Westminster Assembly’s thirty-three chapters, the standard of Presbyterian churches.'),
  ('second-london-baptist-confession','The Second London Baptist Confession (1677/1689)','The Particular Baptists’ revision of Westminster, Baptist on the church and baptism.')]),
 ('arminian','Arminian confessions','The statements of the Remonstrants, the Methodists and the Free Will Baptists.',[
  ('five-articles-of-remonstrance','The Five Articles of Remonstrance (1610)','The founding Arminian statement on election, atonement, grace and perseverance.'),
  ('remonstrant-confession','The Remonstrant Confession (1621)','Simon Episcopius’s full confession of faith for the Remonstrants after Dort.'),
  ('wesley-articles-of-religion','Wesley’s Articles of Religion (1784)','John Wesley’s abridgment of the Thirty-nine Articles for American Methodists.'),
  ('free-will-baptist-treatise','The Free Will Baptist Confession (1834/1868)','The Free-will Baptist confession, with a note on the National Association’s current Treatise.')])]
sec=''
for gid,h,d,items in G:
    li=''.join(f'\n        <li><a href="/creeds/{s}"><span class="ref">{t}</span><span class="meta">{m}</span></a></li>' for s,t,m in items)
    sec+=f'''
      <h2 class="creeds-group-title" id="{gid}">{h}</h2>
      <p class="creeds-group-desc">{d}</p>
      <ul class="passage-list">{li}
      </ul>'''
idx=f'''  <main class="bible-index articles-hub creeds-hub">
    <div class="reader">
      <p class="browse-crumbs"><a href="/">Home</a></p>
      <div class="page-intro page-intro--hub">
        <p class="eyebrow">Historical</p>
        <h1>Creeds &amp; Confessions</h1>
        <p>The creeds the whole church confesses, and the confessions that shaped the Arminian and Reformed traditions.</p>
      </div>
      <p class="creeds-intro">Arminian and Reformed Christians share far more than they dispute: both confess the ancient creeds on the Trinity and the person of Christ, and both teach salvation by grace through faith. They differ on election, the extent of the atonement, how grace works, and whether believers can fall away. Each page below gives the full text in a public-domain English version, with its history, links to the Scriptures it cites, and a short note on where both traditions stand. Each document is presented in its own words; where one answers another, as the Canons of Dort answer the Remonstrance, we link the two.</p>{sec}
    </div>
  </main>
'''
open(OUT+'index.html','w').write(page('Creeds &amp; Confessions','Historic Christian creeds and Arminian and Reformed confessions, with full public-domain texts, background, and Scripture links.','/creeds/',idx))
print('ok', len(order))
