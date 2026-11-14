import json, re
from render import build, card, group, toc, para
from frame import esc
from lib import R, chips, parse, roman
D='/workspace/gt-creeds-mock/mock-src/data/'
def load(n): return json.load(open(D+n+'.json'))['sections']

REM=[('art1','Article I',["That God, by an eternal, unchangeable purpose in Jesus Christ his Son, before the foundation of the world, hath determined, out of the fallen, sinful race of men, to save in Christ, for Christ's sake, and through Christ, those who, through the grace of the Holy Ghost, shall believe on this his Son Jesus, and shall persevere in this faith and obedience of faith, through this grace, even to the end; and, on the other hand, to leave the incorrigible and unbelieving in sin and under wrath, and to condemn them as alienate from Christ, according to the word of the gospel in John iii. 36: 'He that believeth on the Son hath everlasting life: and he that believeth not the Son shall not see life; but the wrath of God abideth on him,' and according to other passages of Scripture also."],["john 3:36"]),
('art2','Article II',["That, agreeably thereto, Jesus Christ, the Saviour of the world, died for all men and for every man, so that he has obtained for them all, by his death on the cross, redemption and the forgiveness of sins; yet that no one actually enjoys this forgiveness of sins except the believer, according to the word of the Gospel of John iii. 16: 'God so loved the world that he gave his only-begotten Son, that whosoever believeth in him should not perish, but have everlasting life.' And in the First Epistle of John ii. 2: 'And he is the propitiation for our sins; and not for ours only, but also for the sins of the whole world.'"],["john 3:16","1-john 2:2"]),
('art3','Article III',["That man has not saving grace of himself, nor of the energy of his free will, inasmuch as he, in the state of apostasy and sin, can of and by himself neither think, will, nor do any thing that is truly good (such as saving Faith eminently is); but that it is needful that he be born again of God in Christ, through his Holy Spirit, and renewed in understanding, inclination, or will, and all his powers, in order that he may rightly understand, think, will, and effect what is truly good, according to the Word of Christ, John xv. 5: 'Without me ye can do nothing.'"],["john 15:5"]),
('art4','Article IV',["That this grace of God is the beginning, continuance, and accomplishment of all good, even to this extent, that the regenerate man himself, without prevenient or assisting, awakening, following and cooperative grace, can neither think, will, nor do good, nor withstand any temptations to evil; so that all good deeds or movements, that can be conceived, must be ascribed to the grace of God in Christ. But as respects the mode of the operation of this grace, it is not irresistible, inasmuch as it is written concerning many, that they have resisted the Holy Ghost. Acts vii., and elsewhere in many places."],["acts 7:51"]),
('art5','Article V',["That those who are incorporated into Christ by a true faith, and have thereby become partakers of his life-giving Spirit, have thereby full power to strive against Satan, sin, the world, and their own flesh, and to win the victory; it being well understood that it is ever through the assisting grace of the Holy Ghost; and that Jesus Christ assists them through his Spirit in all temptations, extends to them his hand, and if only they are ready for the conflict, and desire his help, and are not inactive, keeps them from falling, so that they, by no craft or power of Satan, can be misled nor plucked out of Christ's hands, according to the Word of Christ, John x. 28: 'Neither shall any man pluck them out of my hand.' But whether they are capable, through negligence, of forsaking again the first beginnings of their life in Christ, of again returning to this present evil world, of turning away from the holy doctrine which was delivered them, of losing a good conscience, of becoming devoid of grace, that must be more particularly determined out of the Holy Scripture, before we ourselves can teach it with the full persuasion of our minds."],["john 10:28"]),
('closing','Closing statement',["These Articles, thus set forth and taught, the Remonstrants deem agreeable to the Word of God, tending to edification, and, as regards this argument, sufficient for salvation, so that it is not necessary or edifying to rise higher or to descend deeper."],[])]
DORTLINK={'art1':'<a href="/creeds/canons-of-dort#head1">Dort’s answer: First Head, Divine Predestination</a>','art2':'<a href="/creeds/canons-of-dort#head2">Dort’s answer: Second Head, the Death of Christ</a>','art3':'<a href="/creeds/canons-of-dort#head3">Dort’s answer: Third and Fourth Heads</a>','art4':'<a href="/creeds/canons-of-dort#head3">Dort’s answer: Third and Fourth Heads</a>','art5':'<a href="/creeds/canons-of-dort#head5">Dort’s answer: Fifth Head, Perseverance</a>'}
def remonstrance():
    items=[]
    for k,l,ps,refs in REM:
        note=f'<strong>Answered at Dort.</strong> {DORTLINK[k]}.' if k in DORTLINK else ''
        items.append(card(k,l,None,ps,chips([R(r) for r in refs],3),note))
    return build(dict(slug='five-articles-of-remonstrance',title='The Five Articles of Remonstrance (1610)',desc='The Five Articles of the Remonstrance (1610), the founding statement of Dutch Arminianism, in Philip Schaff’s public-domain translation, with history and links to the Canons of Dort.',
     eyebrow='Arminian Confession',h1='The Five Articles of Remonstrance',sub='The five articles of 1610 in which the followers of Jacob Arminius set out their teaching on election, atonement, grace and perseverance.',
     meta=['The Netherlands, 1610','Text: Schaff’s translation, 1877'],pill='Public domain',
     background=['After Jacob Arminius died in 1609, the leadership of his followers passed to the Leiden professor Simon Episcopius and Johannes Uytenbogaert, a preacher at The Hague. According to Schaff, the five articles were drawn up by Uytenbogaert and presented in 1610, signed by forty-six ministers, to the representatives of Holland and West Friesland; Britannica describes the remonstrance as presented to the States-General. The petition’s name gave the party its name, Remonstrants [[schaff1]] [[b_remonstrant]].',
      'The Calvinist party answered with a Counter-Remonstrance. A conference at The Hague in 1611 and later efforts at peace failed, and the dispute was finally taken up by the national Synod of Dort (1618–19), which rejected the five articles and answered them in its Canons [[schaff1]]. Condemned and expelled at Dort, the Remonstrants were allowed back in the Netherlands by 1630 and officially recognized in 1798; the Remonstrant movement continues today [[b_remonstrant]].'],
     version='The English translation made for Philip Schaff’s <em>Creeds of Christendom</em>, vol. 3 (1877), from the Dutch text of the first edition of 1612. As in Schaff, the petition’s preface, its five “negative” articles (the positions the Remonstrants rejected), and its conclusion are omitted; the brief closing statement he prints is included [[schaff3]]. Scripture links follow the articles’ own references.',
     items=items,
     after_text='''
      <p class="creed-version">For the synod’s reply article by article, see the <a href="/creeds/canons-of-dort#remonstrance-and-dort">Canons of Dort</a>, and for a fuller comparison our article on <a href="/articles/tulip-and-the-remonstrance">TULIP and the Remonstrance</a>.</p>''',
     both=dict(intro='The Remonstrance is the founding Arminian statement; the Canons of Dort are the Reformed reply. Read in their own words, the two agree more than their reputations suggest, especially on human inability and the necessity of grace.',
       arminian=['The articles ground salvation wholly in grace: fallen man “can of and by himself neither think, will, nor do any thing that is truly good,” and grace is “the beginning, continuance, and accomplishment of all good.” What they deny is that this grace is irresistible, and they define election as God’s decree to save believers who persevere [[schaff3]].',
                 'Article V leaves open whether true believers can fall away; Schaff notes that the question was left undetermined [[schaff1]]. Later Arminians, including Episcopius’s confession of 1621, taught that they can [[tcp_remconf]].'],
       reformed=['The Synod of Dort rejected the five articles and answered each in turn [[schaff1]]. The Canons answer Articles III–IV by ascribing the difference between those who believe and those who do not “wholly … to God,” not to “the proper exercise of freewill, whereby one distinguishes himself above others equally furnished with grace sufficient for faith and conversion” (Third and Fourth Heads, Article 10) [[schaff3]].']),
    ))

def remconf():
    rs=load('remconf'); items=[]; tocs=[]
    for i,x in enumerate(rs,1):
        paras=list(x['paras'])
        if x['key']=='conclusion': title='The Conclusion'; label='Conclusion'
        else:
            title=paras.pop(0)[2:].strip().rstrip('.') if paras and paras[0].startswith('##') else x['head']
            label=f'Chapter {i}'
        refs=[c for n in x['notes'] for c in parse(n)]
        items.append(card(x['key'],label,esc(title),paras,chips(refs,3)))
        tocs.append((x['key'],(f'{i}. ' if label!='Conclusion' else '')+esc(title)))
    summary='''
      <h2 id="at-a-glance">At a glance: grace, election and perseverance</h2>
      <p>The Confession is long, and most of it is common Protestant teaching on Scripture, the Trinity, Christ and the Christian life. Its distinctive Arminian teaching is concentrated in a few chapters:</p>
      <ul class="creed-glance">
        <li><a href="#chapter1"><strong>Scripture (Chapter 1).</strong></a> Scripture alone settles controversies of faith; no council, synod or confession may bind consciences by its own authority, though the interpretations of the ancient fathers are to be respected.</li>
        <li><a href="#chapter8"><strong>Christ’s redemption (Chapter 8).</strong></a> The merit of Christ has a universal force; the Confession argues that an absolute election and reprobation decreed before Christ was appointed Mediator would undo it.</li>
        <li><a href="#chapter17"><strong>Grace and calling (Chapter 17).</strong></a> Grace is “the beginning, progress, and complement of all good,” without which no one can believe; God gives grace sufficient for faith to all who are called by the gospel, and calls them seriously; yet a person “may despise and reject the Grace of God, and resist the operation of it.”</li>
        <li><a href="#chapter18"><strong>Election and perseverance (Chapter 18).</strong></a> “Election unto glory” belongs to those who already truly believe. God’s saving acts toward them continue as long as the condition of faith and holiness endures and “are interrupted when we no longer stand to our Covenants.”</li>
        <li><a href="#chapter25"><strong>Synods and toleration (Chapter 25).</strong></a> Synods should judge only by the Word of God, with full liberty to speak, and the magistrate should not enforce their decrees by fines, banishment, imprisonment or death.</li>
      </ul>
      <p class="creed-version">Quotations are from the 1676 English translation [[tcp_remconf]].</p>'''
    return build(dict(slug='remonstrant-confession',title='The Remonstrant Confession (1621)',desc='The Confession of the Remonstrants (1621), prepared by Simon Episcopius, in the 1676 English translation, with history, a summary of its key chapters, and where Arminian and Reformed churches stand.',
     eyebrow='Arminian Confession',h1='The Remonstrant Confession',sub='The confession of faith of the Dutch Remonstrants, written by Simon Episcopius after the Synod of Dort.',
     meta=['Simon Episcopius, 1621 (Latin 1622)','Text: English translation, London, 1676'],pill='Public domain',
     background=['Simon Episcopius (1583–1643) became professor of theology at Leiden in 1612. He was one of the thirteen Remonstrants summoned before the Synod of Dort [[schaff1]], after which he and the others were banished; he lived in exile in Paris, Antwerp and Rouen until 1626, and from 1634 headed the Remonstrant seminary in Amsterdam [[b_episcopius]]. In opposition to the Canons of Dort he prepared a defense of the Arminian articles and this confession of faith, published in Dutch in 1621 and in Latin in 1622 [[schaff1]].',
      'Schaff notes that the Confession “claims no binding symbolical authority, and advocates liberty and toleration” [[schaff1]]. Unlike the five short articles of 1610, it covers the whole of Christian doctrine in twenty-five chapters. An English translation was printed in London in 1676 [[tcp_remconf]].'],
     after_bg=summary,
     version='The English translation printed in London in 1676 (Wing T564), transcribed by the Text Creation Partnership and released into the public domain [[tcp_remconf]]. Original spelling and capitals are kept, with the long “s” modernized. The transcribers could not read some letters in the copy they used. Each of these gaps was checked against page images of the 1676 edition (a UMI microfilm scan) [[sea_scan]]; thirteen could be read there and are filled in. The rest are lost in the binding or in damaged or faded print and stay marked: a bullet (•) for illegible letters and […] for a longer illegible word or passage. The preface is not included. Scripture links are drawn from the Confession’s own marginal references, up to three per chapter.',
     toc=toc(tocs), items=items,
     both=dict(intro='This is the Remonstrants’ own positive statement of faith after Dort. It is useful to both traditions because it shows what the condemned party actually affirmed, in its own words.',
       arminian=['Chapter 17’s pairing of total dependence on grace with resistible grace is the classic Arminian position, and Chapter 18’s conditional perseverance answers the question the 1610 Remonstrance had left open [[tcp_remconf]] [[schaff1]]. Its insistence that confessions do not bind the conscience (Chapters 1 and 25) became a lasting mark of the Remonstrant tradition [[schaff1]].'],
       reformed=['Reformed readers can agree with much of the Confession, including its teaching that grace is necessary for every saving good. They part from it on election, which the Confession places after faith (“Election unto glory” of those who already believe), whereas the Canons of Dort say election “was not founded upon foreseen faith” (First Head, Article 9); and on its teaching that believers’ saving benefits can be “interrupted,” whereas the Canons teach that God preserves his own so that they do not finally fall away (Fifth Head, Article 8) [[schaff3]].']),
    ))

MA={1:["matthew 28:19","1-timothy 1:17"],2:["john 1:14","philippians 2:6","hebrews 2:17"],3:["luke 24:39","acts 1:11"],4:["john 15:26"],5:["2-timothy 3:16","2-peter 1:21"],6:["luke 24:27","john 5:39"],
7:["romans 5:12","ephesians 2:3"],8:["john 6:44","philippians 2:13","titus 2:11"],9:["romans 3:28","romans 5:1","galatians 2:16"],10:["james 2:18","ephesians 2:10","matthew 7:17"],11:["luke 17:10"],
12:["1-john 1:9","galatians 6:1"],13:["acts 2:42","ephesians 4:4"],16:["romans 4:11","matthew 28:19"],17:["matthew 28:19","acts 2:38"],18:["1-corinthians 10:16","1-corinthians 11:23"],19:["1-corinthians 11:25"],
20:["hebrews 10:12","1-john 2:2"],21:["hebrews 13:4"],22:["1-corinthians 14:40"],23:["romans 13:1","1-peter 2:13"],24:["acts 5:4","ephesians 4:28"],25:["matthew 5:34","james 5:12"]}
def wesley():
    ms=load('methodist')[2:]; arts=[]
    for x in ms:
        t=x['t']; m=re.match(r'^([IVXL]+)\. (.*)$',t)
        if m and t.upper()==t: arts.append([roman(m.group(1)),m.group(2).rstrip('.'),[]])
        else: arts[-1][2].append(t)
    small={'of','the','and','in','to','a','as','such','for','or','upon','who','was'}
    def tc(s): 
        w=s.lower().split(); return ' '.join(x if (i and x in small) else x[:1].upper()+x[1:] for i,x in enumerate(w)).replace("Men's","Men’s").replace("Man's","Man’s").replace("Lord's","Lord’s").replace('United States Of America','United States of America')
    items=[]; tocs=[]
    for n,t,ps in arts:
        note=''
        if n==23: note='<strong>Article 23.</strong> This article was not part of the Church of England’s Articles. Schaff dates its adoption by the Methodist Episcopal Church to 1804 [[schaff3]]; other accounts say it was added at the Christmas Conference of 1784 [[bt_articles]]. The wording printed here is that of the 1872 <em>Discipline</em>.'
        items.append(card(f'art{n}',f'Article {n}',tc(t),ps,chips([R(r) for r in MA.get(n,[])],3),note))
        tocs.append((f'art{n}',f'{n}. {tc(t)}'))
    return build(dict(slug='wesley-articles-of-religion',title='The Methodist Articles of Religion (1784)',desc='John Wesley’s Articles of Religion for American Methodists (1784), in full from the 1872 Methodist Episcopal Discipline as printed by Philip Schaff, with history, Scripture links, and where both traditions stand.',
     eyebrow='Arminian Confession',h1='Wesley’s Articles of Religion',sub='John Wesley’s abridgment of the Church of England’s Thirty-nine Articles for the Methodists in America.',
     meta=['Christmas Conference, Baltimore, 1784','Text: Methodist Episcopal <em>Discipline</em>, 1872'],pill='Public domain',
     background=['After American independence, John Wesley provided the Methodists in America with a liturgy, <em>The Sunday Service of the Methodists in North America</em>, and a doctrinal statement, the Articles of Religion, his revision of the Thirty-nine Articles. The American preachers gathered at Baltimore in December 1784, the “Christmas Conference,” adopted both in forming the Methodist Episcopal Church [[umc_standards]].',
      'Wesley omitted fifteen of the Thirty-nine Articles, among them Article 17, “Of Predestination and Election”; Schaff describes the result as an abridgment with “the Calvinistic and other features being omitted” [[schaff3]]. The General Conference of 1808 made the Articles the church’s explicit doctrinal standard and forbade any change to them by its first Restrictive Rule [[umc_standards]]. They remain the Articles of Religion of the United Methodist Church [[umc_articles]].'],
     version='The text printed by Philip Schaff in <em>The Creeds of Christendom</em>, vol. 3 (1877), from <em>The Doctrines and Discipline of the Methodist Episcopal Church</em> (New York, 1872) [[schaff3]]. Schaff notes that the articles “underwent some changes, chiefly verbal,” after 1784. Article headings are given in title case. Scripture links are passages chosen for this page; the Articles cite no proof texts.',
     toc=toc(tocs), items=items,
     both=dict(intro='Because the Articles are an abridgment of an Anglican confession that both traditions respect, most of their text is shared ground. What is distinctive is chiefly what Wesley left out.',
       arminian=['Article 8, “Of Free Will,” teaches that fallen man “can not turn and prepare himself, by his own natural strength and works, to faith and calling upon God,” and has no power to do good works “without the grace of God by Christ preventing us, that we may have a good will, and working with us” [[schaff3]]. “Preventing” here has its older sense of “going before.” Article 12 says that “we may depart from grace given, and fall into sin, and, by the grace of God, rise again” [[schaff3]].',
                 'The United Methodist Church’s own account notes that the Articles lack several distinctive Wesleyan emphases, such as assurance and Christian perfection, which Methodists find in Wesley’s Sermons and Notes [[umc_standards]].'],
       reformed=['Reformed Anglicans hold the full Thirty-nine Articles, including Article 17, which teaches predestination to life as “the everlasting purpose of God” [[schaff3]]. They would read Article 8, which Wesley kept, as consistent with Reformed teaching on human inability; Article 12 is likewise kept from the Anglican original. Much of the difference therefore lies in what the Articles leave unsaid about election, rather than in what they affirm [[schaff3]].']),
    ))

FW={1:["2-timothy 3:16","2-peter 1:21"],2:["john 4:24","1-timothy 1:17"],3:["matthew 10:29","acts 17:26"],4:["genesis 1:1","genesis 1:27","romans 5:12"],5:["john 1:1","john 1:14","colossians 2:9"],
6:["acts 5:3","1-corinthians 2:10"],7:["hebrews 9:22","1-john 2:2","hebrews 7:25"],8:["1-timothy 2:4","1-john 2:2","revelation 22:17"],9:["acts 17:30","2-corinthians 7:10"],10:["romans 10:17","hebrews 11:6"],
11:["john 3:3","titus 3:5"],12:["romans 5:1","1-thessalonians 4:3"],13:["hebrews 6:4","1-timothy 1:19","1-peter 1:5"],14:["revelation 1:10","acts 20:7"],15:["acts 2:42","1-corinthians 1:2"],
16:["1-timothy 3:2","2-timothy 4:2"],17:["matthew 28:19","romans 6:4","1-corinthians 11:23"],18:["2-corinthians 5:8","luke 23:43"],19:["acts 1:11","1-thessalonians 4:16"],20:["john 5:28","1-corinthians 15:52"],21:["2-corinthians 5:10","matthew 25:46"]}
def fwb():
    fs=load('fwb')[2:]; chs=[]
    for x in fs:
        t=x['t'].replace('l’','V').replace('PRIMITIl’E','PRIMITIVE')
        m=re.match(r'^CHAPTER ([IVXL]+)\.$',t)
        if m: chs.append([roman(m.group(1)),None,[]]); continue
        if chs[-1][1] is None: chs[-1][1]=t.rstrip('.'); continue
        sm=re.match(r'^SECTION ([IVX]+)\.(?:—(.*))?$',t)
        if sm: chs[-1][2].append('##Section '+sm.group(1)+('. '+sm.group(2).title().replace(' Of ',' of ').replace(' And ',' and ') if sm.group(2) else '')); continue
        chs[-1][2].append(t)
    items=[]; tocs=[]
    for n,t,ps in chs:
        note=''
        if n in (3,8,13):
            note='<strong>Distinctive.</strong> Schaff prints '+('sections 2 and 3 of this chapter' if n==3 else 'this chapter')+' in italics as one of the places where this confession differs from earlier Baptist confessions [[schaff3]].'
        items.append(card(f'ch{n}',f'Chapter {n}',esc(t),ps,chips([R(r) for r in FW.get(n,[])],3),note))
        tocs.append((f'ch{n}',f'{n}. {esc(t)}'))
    assert len(chs)==21, len(chs)
    current='''
      <h2 id="current-treatise">The National Association’s Treatise today</h2>
      <p>The text above is the nineteenth-century northern confession. The National Association of Free Will Baptists, organized in 1935, has its own <em>Treatise of the Faith and Practices</em>. It is copyrighted, so we summarize it rather than reprint it [[nafwb_treatise]].</p>
      <ul class="creed-glance">
        <li>It was adopted when the National Association was organized at Nashville in November 1935 and has been revised many times since; the 2026 edition lists revisions from 1948 to 2026 [[nafwb_treatise]].</li>
        <li>Its doctrinal part keeps the outline and much of the wording of the older confession, including the chapters on the gospel call and on perseverance, now with numbered Scripture proofs [[nafwb_treatise]].</li>
        <li>It differs in places. It has twenty-two chapters rather than twenty-one, adding a chapter on tithing; it lists washing the saints’ feet among the ordinances of the gospel; and its chapter on sanctification describes continuing growth in grace rather than cleansing “from all sin” [[nafwb_treatise]].</li>
      </ul>'''
    return build(dict(slug='free-will-baptist-treatise',title='The Free Will Baptist Confession (1834/1868)',desc='The Free-will Baptist Confession of 1834, as revised in 1868, in the public-domain text printed by Philip Schaff, with history, a note on the National Association’s current Treatise, Scripture links, and where both traditions stand.',
     eyebrow='Arminian Confession',h1='The Free Will Baptist Confession',sub='The doctrinal chapters of the Free-will Baptist <em>Treatise</em>: Baptist in church order, Arminian in its teaching on grace.',
     meta=['General Conference, 1834; revised 1868','Text: <em>Treatise</em>, Dover, N.H., 1871'],pill='Public domain',
     background=['Free Will Baptists in America descend from two lines. In the South, Paul Palmer organized a church at Chowan, North Carolina, in 1727; in the North, Benjamin Randall organized a congregation at New Durham, New Hampshire, on June 30, 1780. Both taught “free grace, free salvation and free will,” though at first there was no connection between them [[nafwb_hist]].',
      'The confession printed here belongs to the northern line. Its General Conference adopted it in 1834 and revised it in 1848, 1865 and 1868 [[schaff3]]. In 1910–11 that body merged with the Northern Baptists, taking more than half of its churches; remnant churches reorganized in 1916, and on November 5, 1935, at Nashville, they joined with the southern Free Will Baptists to form the National Association of Free Will Baptists, which adopted a treatise of its own [[nafwb_hist]].'],
     version='The text printed by Philip Schaff in <em>The Creeds of Christendom</em>, vol. 3 (1877), from the <em>Treatise on the Faith and Practice of the Free-will Baptists</em> (Dover, N.H., 1871) [[schaff3]]. Obvious scanning errors in chapter numbers and headings are corrected. Scripture links are passages chosen for this page; Schaff does not print the Treatise’s proof texts.',
     toc=toc(tocs), items=items, after_text=current,
     both=dict(intro='This confession is plainly Arminian on grace and Baptist on the church. It shares with Reformed Baptists the immersion of believers, and with all Protestants the core doctrines of God, Christ and justification.',
       arminian=['Its distinctive chapters say that God “has endowed man with power of free choice” and that his foreknowledge does not cause events (Chapter 3); that the gospel call is “co-extensive with the atonement to all men,” so that “salvation is rendered equally possible to all” (Chapter 8); and that believers’ “future obedience and final salvation are neither determined nor certain” (Chapter 13) [[schaff3]].'],
       reformed=['Reformed Baptists share this confession’s view of baptism as the immersion of believers, which the Second London Confession also teaches [[tcp_lbcf]]. They differ on the extent and effect of the atonement and on perseverance, where the Second London Confession, following Westminster, teaches that true believers “can neither totally nor finally fall from the state of grace; but shall certainly persevere therein to the end” [[tcp_lbcf]].']),
    ))

if __name__=='__main__':
    import sys
    for n in sys.argv[1:]: print(n, globals()[n]())
