import json, re
from render import build, card, group, toc, para
from frame import esc
from lib import R, chips, parse, ccel
D='/workspace/gt-creeds-mock/mock-src/data/'
def load(n): return json.load(open(D+n+'.json'))['sections']
def slugify(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def titlecase(t):
    t=t.replace(' OP ',' OF ').replace('OP THE','OF THE').replace(' PROM ',' FROM ').replace("CHRIST' ","CHRIST'S ")
    small={'of','the','and','in','to','a','an','by','for','unto','is','are','what','from','or','be','his','our','its','yet','with','we','us'}
    w=t.lower().split(' ')
    return ' '.join(x if (i and x in small) else x[:1].upper()+x[1:] for i,x in enumerate(w)).replace("Man's","Man’s").replace("Christ's","Christ’s").replace("'","’")

HC={1:["1-corinthians 6:19","romans 14:8","john 6:39"],2:["romans 3:23","john 17:3","ephesians 5:8"],3:["romans 3:20"],4:["matthew 22:37"],5:["romans 3:10","romans 8:7"],
6:["genesis 1:26"],7:["romans 5:12"],8:["john 3:5","ephesians 2:1"],9:["ephesians 4:24"],10:["romans 5:12","hebrews 9:27"],12:["romans 8:3"],15:["hebrews 2:17","1-timothy 2:5"],
18:["1-corinthians 1:30","1-timothy 2:5"],20:["john 1:12","romans 11:20"],21:["hebrews 11:1","ephesians 2:8","romans 4:16"],26:["genesis 1:1","romans 8:15"],27:["hebrews 1:3","matthew 10:29"],
29:["matthew 1:21","acts 4:12"],31:["acts 3:22","hebrews 7:24","revelation 19:16"],33:["john 1:14","romans 8:15"],37:["1-peter 2:24","isaiah 53:5"],44:["matthew 27:46"],
45:["romans 4:25","romans 6:4"],46:["acts 1:9"],52:["philippians 3:20","matthew 25:31"],53:["john 14:16","2-corinthians 13:14"],54:["john 10:28","ephesians 1:10","1-john 3:21"],
56:["2-corinthians 5:19","ephesians 1:7"],57:["philippians 1:23","1-corinthians 15:53"],58:["1-corinthians 2:9"],60:["romans 3:24","ephesians 2:8","titus 3:5"],61:["1-corinthians 1:30"],
63:["luke 17:10"],64:["matthew 7:18"],65:["romans 10:17"],66:["romans 4:11"],69:["matthew 28:19","acts 2:38"],72:["1-john 1:7"],74:["acts 2:39"],75:["1-corinthians 11:23","matthew 26:26"],
80:["hebrews 9:12","hebrews 10:12"],86:["romans 6:13","1-peter 2:9","matthew 5:16"],88:["romans 6:4","colossians 3:5"],91:["romans 14:23","colossians 3:17"],
92:["exodus 20:2"],94:["matthew 4:10"],103:["acts 2:42"],105:["matthew 5:21"],113:["romans 7:7"],114:["1-john 1:8","romans 7:14"],115:["romans 3:20","philippians 3:12"],
116:["matthew 7:7","luke 11:9"],117:["john 4:24","psalms 145:18"],119:["matthew 6:9"],120:["matthew 7:9"],129:["2-corinthians 1:20","revelation 22:20"]}
LDSTART=[1,3,6,9,12,16,20,24,26,27,29,31,33,35,37,40,45,46,50,53,54,57,59,62,65,69,72,75,78,80,83,86,88,92,96,99,101,103,104,105,108,110,112,113,116,120,122,123,124,125,126,127]
assert len(LDSTART)==52
def heidelberg():
    hs=load('heidelberg'); items=[]; tocs=[]; cur=None
    for x in hs:
        n=int(x['key'][1:])
        g=(x['part'] or 'Introduction', x['head'])
        if g!=cur:
            if g[0]!=(cur or (None,))[0]:
                gid=slugify(g[0]); items.append(group(gid, esc(g[0]).replace("'","’"))); tocs.append((gid, esc(g[0].split(': ')[-1]).replace("'","’")+f' <span class="creed-toc-range">from Q{n}</span>'))
            if g[1]:
                sid=slugify(g[1]); items.append(f'\n      <p class="creed-subgroup" id="{sid}">{esc(g[1])}</p>'); tocs.append((sid,'&nbsp;&nbsp;&nbsp;'+esc(g[1])+f' <span class="creed-toc-range">from Q{n}</span>'))
            cur=g
        if n in LDSTART:
            d=LDSTART.index(n)+1
            items.append(f'\n      <p class="creed-ld" id="lords-day-{d}">Lord’s Day {d}</p>')
        a=list(x['a']); note=''
        if x['paren']:
            a=[p.strip('()') for p in a]
            note='<strong>Question 80.</strong> This question was not in the first edition of 1563. Schaff reports that the second edition had it in part and the third in full, inserted by command of the Elector Frederick III; the words in square brackets are the third-edition additions [[schaff1]]. In 2004 the Christian Reformed Church in North America declared that Q&amp;A 80 “can no longer be held in its current form as part of our confession,” and in 2006 it bracketed the last paragraphs as not binding on its members; the Reformed Church in America retains the full original text [[crc_hc]].'
        paras=''.join('\n          '+(f'<p class="creed-subhead">{esc(p[1:])}</p>' if p.startswith('§') else para(p)) for p in a)
        items.append(card(x['key'],f'Question {n}',q=x['q'].replace('(',''),raw=paras,chips=chips([R(r) for r in HC.get(n,[])],3),note=note))
    return build(dict(slug='heidelberg-catechism',title='The Heidelberg Catechism (1563)',desc='The Heidelberg Catechism (1563) in full, in the public-domain English text printed by Philip Schaff, with history, Scripture links, and where Arminian and Reformed churches stand.',
     eyebrow='Reformed Catechism',h1='The Heidelberg Catechism',sub='129 questions and answers on comfort in Christ: our sin and misery, our redemption, and our thankfulness.',
     meta=['Heidelberg, 1563','Text: Schaff, <em>Creeds of Christendom</em>, 1877'],pill='Public domain',
     background=['The catechism was written in 1562, chiefly by Caspar Olevianus and Zacharias Ursinus, as part of the reform program of Frederick III, Elector Palatine, and was accepted by the synod of the Palatinate church in 1563. Britannica describes it as practical and devotional in tone, with predestination “very mildly stated” [[b_heidelberg]].',
      'Three German editions appeared in 1563; the second and third added Question 80 on the Mass. The later division into fifty-two “Lord’s Days,” one for each Sunday of the year, followed the example of Calvin’s Genevan catechism [[schaff1]]. The Synod of Dort (1618–19) adopted it together with the Belgic Confession and its own Canons [[schaff1]], and the three remain the doctrinal basis of the Dutch Reformed churches and of the Christian Reformed Church [[b_dort]].'],
     version='The English translation printed by Philip Schaff in <em>The Creeds of Christendom</em>, vol. 3 (1877), beside the German [[schaff3]]. Schaff does not number the Lord’s Days. The text is arranged here by its three parts and the headings he prints, and the fifty-two Lord’s Days are marked using the standard division, as numbered in the editions of the Christian Reformed Church in North America and the Reformed Church in America [[crc_hc]] [[rca_hc]]. Scripture links are a small selection chosen for this page, not the catechism’s own proof texts; they open our verse-by-verse commentary.',
     toc=toc(tocs)+'\n      <nav class="creed-ld-index" aria-label="Lord’s Days"><span class="creed-toc-title">Lord’s Days</span> '+' '.join(f'<a href="#lords-day-{d}">{d}</a>' for d in range(1,53))+'</nav>', items=items,
     both=dict(intro='The catechism is a Reformed document, but much of it is common ground: its exposition of the Apostles’ Creed, the Ten Commandments and the Lord’s Prayer is close to what Arminian churches teach.',
       arminian=['Jacob Arminius, himself a minister of the Dutch Reformed Church, advocated a revision of the Belgic Confession and the Heidelberg Catechism [[schaff1]]. The Synod of Dort, which rejected the Five Articles of the Remonstrance, adopted the catechism, with the Belgic Confession, as a standard of doctrine [[schaff1]].'],
       reformed=['The division into Lord’s Days arranged the catechism for teaching through the year [[schaff1]], and it remains a confession of the Dutch Reformed churches and the Christian Reformed Church [[b_dort]]. Question 54 speaks of the church as “a chosen communion” gathered by the Son of God, and Question 1 of being preserved so that “all things must work together for my salvation” [[schaff3]].']),
    ))

BC={1:["john 4:24","1-timothy 1:17"],2:["romans 1:20","psalms 19:1"],3:["2-peter 1:21","2-timothy 3:16"],5:["1-thessalonians 2:13"],7:["galatians 1:8","revelation 22:18"],
8:["matthew 28:19","2-corinthians 13:14"],10:["john 1:1","colossians 1:15"],11:["acts 5:3","1-corinthians 3:16"],12:["genesis 1:1","hebrews 11:3"],13:["matthew 10:29","romans 8:28"],
14:["genesis 1:26","romans 5:12","ephesians 2:1"],15:["romans 5:12","psalms 51:5"],16:["ephesians 1:4","romans 9:15","2-timothy 1:9"],17:["genesis 3:15"],18:["galatians 4:4","hebrews 2:14"],
19:["john 1:14","colossians 2:9"],20:["romans 3:25","romans 8:32"],21:["hebrews 9:12","isaiah 53:5","1-peter 2:24"],22:["romans 3:28","galatians 2:16"],23:["romans 4:6","romans 5:1"],
24:["ephesians 2:10","james 2:18","titus 3:8"],25:["colossians 2:17","galatians 5:1"],26:["1-timothy 2:5","hebrews 4:15","1-john 2:1"],27:["ephesians 4:4","matthew 16:18"],28:["hebrews 10:25"],
29:["john 10:27","ephesians 2:20"],30:["acts 6:3","titus 1:5"],31:["1-timothy 3:1"],32:["1-corinthians 14:40"],33:["romans 4:11"],34:["matthew 28:19","colossians 2:11","acts 2:39"],
35:["1-corinthians 11:23","john 6:55"],36:["romans 13:1","1-timothy 2:1"],37:["acts 17:31","matthew 25:31","2-thessalonians 1:7"]}
from lib import roman
def belgic():
    bs=load('belgic'); items=[]; tocs=[]
    for x in bs:
        n=roman(x['key'][3:]); t=titlecase(x['title'])
        refs=[c for p in x['paras'] for c in parse(p)]+[R(r) for r in BC.get(n,[])]
        items.append(card(x['key'],f'Article {n}',t,x['paras'],chips(refs,3)))
        tocs.append((x['key'],f'{n}. {t}'))
    return build(dict(slug='belgic-confession',title='The Belgic Confession (1561)',desc='The Belgic Confession of Guido de Brès (1561), in full in the public-domain English text printed by Philip Schaff, with history, Scripture links, and where Arminian and Reformed churches stand.',
     eyebrow='Reformed Confession',h1='The Belgic Confession',sub='Thirty-seven articles written for the persecuted Reformed churches of the Low Countries.',
     meta=['Guido de Brès, 1561; revised at Dort, 1619','Text: Schaff, <em>Creeds of Christendom</em>, 1877'],pill='Public domain',
     background=['Guido de Brès wrote the confession in French in 1561 for the Reformed churches of Flanders and the Netherlands. A copy was sent to King Philip II of Spain in 1562, and the text was revised at a synod in Antwerp in 1566. De Brès was put to death for his faith in 1567 [[crc_belgic]].',
      'A Reformed synod at Emden adopted the confession in 1571, and the National Synod of Dort (1618–19) adopted it after revising the text by comparing French, Dutch and Latin copies [[schaff3]]. It remains a doctrinal standard of the Dutch Reformed churches and the Christian Reformed Church [[b_dort]].'],
     version='The English text printed by Philip Schaff in <em>The Creeds of Christendom</em>, vol. 3 (1877): the translation authorized by the Reformed (Dutch) Church in America, made from the Latin [[schaff3]]. Article headings are supplied from the Latin editions, as in Schaff. Scripture links are a selection: the article’s own explicit references where it gives them, otherwise passages chosen for this page.',
     toc=toc(tocs), items=items,
     both=dict(intro='Most of the confession is shared Protestant teaching on Scripture, the Trinity, Christ, justification by faith and the church. The traditions part chiefly over Article 16, on election.',
       arminian=['Jacob Arminius, a minister and professor in the Dutch church that held this confession, advocated revising it, along with the Heidelberg Catechism [[schaff1]]. Arminians affirm its teaching that we are justified by faith alone in Christ (Articles 22–23), but read election in Christ, as the Remonstrance of 1610 does, as God’s decree to save “those who, through the grace of the Holy Ghost, shall believe on this his Son Jesus, and shall persevere in this faith” [[schaff3]].'],
       reformed=['Article 16 confesses that God is “merciful, since he delivers and preserves from this perdition all whom he, in his eternal and unchangeable council, of mere goodness hath elected in Christ Jesus our Lord, without any respect to their works: just, in leaving others in the fall and perdition wherein they have involved themselves” [[schaff3]]. The Synod of Dort, which revised and adopted the confession, set out the same doctrine at length in the First Head of its Canons [[schaff1]].']),
    ))

DORTMAP='''
      <h2 id="remonstrance-and-dort">The Remonstrance and the Canons, point by point</h2>
      <p>The synod rejected the five articles the Remonstrants had presented in 1610 and adopted five canons in their place [[schaff1]], arranged under heads of doctrine that answer the articles in order. Each side is quoted here in its own words.</p>
      <div class="creed-table-wrap"><table class="creed-table">
        <thead><tr><th>Remonstrance (1610)</th><th>Canons of Dort (1619)</th></tr></thead>
        <tbody>
          <tr><td><a href="/creeds/five-articles-of-remonstrance#art1">Article I</a>: God decreed to save “those who, through the grace of the Holy Ghost, shall believe on this his Son Jesus, and shall persevere in this faith.”</td><td><a href="#head1">First Head</a>, Divine Predestination: election is “the unchangeable purpose of God” to choose “a certain number of persons to redemption in Christ” (Article 7).</td></tr>
          <tr><td><a href="/creeds/five-articles-of-remonstrance#art2">Article II</a>: Christ “died for all men and for every man,” yet “no one actually enjoys this forgiveness of sins except the believer.”</td><td><a href="#head2">Second Head</a>, the Death of Christ: his death is “abundantly sufficient to expiate the sins of the whole world” (Article 3), and its saving efficacy extends to “all the elect” (Article 8).</td></tr>
          <tr><td><a href="/creeds/five-articles-of-remonstrance#art3">Articles III–IV</a>: without grace fallen man can do nothing truly good; grace is “the beginning, continuance, and accomplishment of all good,” but “it is not irresistible.”</td><td><a href="#head3">Third and Fourth Heads</a>, Corruption and Conversion: that some obey the call “must be wholly ascribed to God,” who confers faith and repentance on his own (Article 10).</td></tr>
          <tr><td><a href="/creeds/five-articles-of-remonstrance#art5">Article V</a>: Christ keeps believers who are ready for the conflict; whether they can fall away “must be more particularly determined out of the Holy Scripture.”</td><td><a href="#head5">Fifth Head</a>, Perseverance: falling away, possible in themselves, is “with respect to God … utterly impossible” (Article 8).</td></tr>
        </tbody>
      </table></div>
      <p class="creed-version">Quotations are from the English texts printed by Schaff [[schaff3]]. For a fuller comparison, see our article on <a href="/articles/tulip-and-the-remonstrance">TULIP and the Remonstrance</a>.</p>'''
def roe_html(t):
    t=t.replace('&c','&amp;c')
    return re.sub(r'\*([^*]+)\*',r'<em>\1</em>',t)
def roe(hn,items,tocs):
    from dort_roe import HEADS
    k=hn.split('–')[0]; h=HEADS[k]; gid=f'head{k}-rejection'
    items.append(group(gid,f'Head {hn}: Rejection of Errors',f'<br>Thomas Scott’s translation (1818), {h["page"]} of the 1831 reprint'))
    tocs.append((gid,f'Head {hn}: Rejection of Errors'))
    for i,(t,note) in enumerate(h['arts'],1):
        intro=f'\n          <p class="creed-para"><em>{h["intro"]}</em></p>' if i==1 else ''
        raw=intro+f'\n          <p class="creed-para"><strong class="creed-num">{i}.</strong> {roe_html(t)}</p>'
        nt=('<strong>Editorial note.</strong> '+note) if note else ''
        items.append(card(f'head{k}-rej{i}',f'Head {hn}, Rejection of Errors {i}',None,(),(),nt,raw=raw))
def dort():
    ds=load('dort'); items=[]; tocs=[]; hn=None
    hmap={'h0':('1','head1'),'h19':('2','head2'),'h29':('3–4','head3'),'h47':('5','head5')}
    for x in ds:
        if x.get('kind')=='head':
            if hn: roe(hn,items,tocs)
            hn,hid=hmap[x['key']]
            x['title']=x['title'].replace(' Of ',' of ').replace(' And ',' and ')
            items.append(group(hid,esc(x['title']),f'<br>{esc(x["sub"])}' if x.get('sub') else ''))
            tocs.append((hid,f'{esc(x["title"])}: {esc(x.get("sub",""))}'))
            continue
        if x['key']=='conclusion':
            roe(hn,items,tocs)
            items.append(group('conclusion','Conclusion')); tocs.append(('conclusion','Conclusion'))
            items.append(card('conclusion-text','Conclusion',None,x['paras']))
            continue
        n=roman(x['key'].split('-')[1])
        refs=[c for c in (ccel(tuple(c)) for c in x['cites']) if c]+chips([c for p in x['paras'] for c in parse(p)],3)
        ch=[]; seen=set()
        for h,l in refs:
            pg=h.split('#')[0]
            if pg not in seen: seen.add(pg); ch.append((h,l))
        kid=f'head{hn.split("–")[0]}-art{n}'
        items.append(card(kid,f'Head {hn}, Article {n}',None,x['paras'],ch[:2]))
    return build(dict(slug='canons-of-dort',title='The Canons of Dort (1619)',desc='The Canons of the Synod of Dort (1618–19) in the public-domain English text printed by Philip Schaff, with the Rejection of Errors in Thomas Scott’s 1818 translation, history, the Remonstrance point by point, Scripture links, and where both traditions stand.',
     eyebrow='Reformed Confession',h1='The Canons of Dort',sub='The Synod of Dort’s answer to the five articles of the Remonstrants, arranged under five heads of doctrine.',
     meta=['Synod of Dort, 1618–19','Text: Schaff, <em>Creeds of Christendom</em>, 1877; Rejection of Errors: Scott, 1818'],pill='Public domain',
     background=['After the death of Jacob Arminius in 1609, his followers set out their views in the Remonstrance of 1610. Schaff notes that the dispute, though theological, became entangled in the politics of the Dutch Republic because of the close connection of church and state [[schaff1]]. The States-General called a national synod, which met at Dordrecht (Dort) from November 13, 1618, to May 9, 1619. It had eighty-four members and eighteen secular commissioners; fifty-eight were Dutch, and the rest came from Reformed churches abroad. King James I sent English delegates; the French Reformed chose delegates, but their king forbade them to leave the country [[schaff1]] [[b_dort]].',
      'Simon Episcopius and twelve other Remonstrants were summoned before the synod as defendants rather than members. They protested against the conditions imposed on them [[schaff1]] and were expelled [[b_dort]]. The synod rejected the five Remonstrant articles and adopted its own canons, together with the Belgic Confession and the Heidelberg Catechism. About two hundred Remonstrant ministers were afterward deposed. The Remonstrant statesman Johan van Oldenbarnevelt was beheaded on a charge of high treason on May 14, 1619; Schaff calls the arrest of the Remonstrant political leaders “independent” of the synod, while judging the condemnation unjust [[schaff1]].'],
     after_bg=DORTMAP,
     version='The articles under each head and the Conclusion are the English text printed by Philip Schaff in <em>The Creeds of Christendom</em>, vol. 3 (1877), as adopted by the Reformed (Dutch) Church in America [[schaff3]]. Words in square brackets in those articles are Schaff’s, restoring phrases of the Latin that the American translation left out [[schaff3]]. The synod’s Preface and its Sentence against the Remonstrants are not reproduced. The “Rejection of Errors” after each head is not part of Schaff’s English text. It is given here from the translation by Thomas Scott, first published in London in 1818 and reprinted at Utica, New York, in 1831 [[scott]]; Scott died in 1821, and the translation is in the public domain. It has been proofread against the page images of the 1831 reprint and compared with the Latin in Schaff [[schaff3]]. Scott’s footnotes and remarks are left out, as are a few proof texts he added inside the articles that are not in the Latin; each such omission, and each obvious misprint corrected, is noted under the article, and a mistaken reference is followed by the Latin’s reference as “[read …]”. Words in parentheses and italics are Scott’s glosses from the Latin. Because the two parts come from different translators, their wording and style differ. The Reformed Church in America does not give confessional status to the Rejection of Errors, though it recognizes that they help interpret the Canons [[crc_dort]]. Scripture links are references the articles themselves make, up to two per article.',
     toc=toc(tocs,cols=False), items=items,
     both=dict(intro='The Canons are the Reformed side of the debate, written in reply to the Arminian articles. They also contain common ground that is easily missed, including the infinite worth of Christ’s death and the command to preach the gospel to all.',
       arminian=['The Remonstrants were summoned as defendants rather than members, and protested against the conditions imposed on them [[schaff1]]. Their leader Episcopius then prepared a confession of their own, published in Dutch in 1621; see the <a href="/creeds/remonstrant-confession">Remonstrant Confession</a> [[schaff1]].',
                 'On the need for grace the Remonstrance agrees with the Canons: fallen man “can of and by himself neither think, will, nor do any thing that is truly good.” The parting comes over whether that grace is irresistible (Articles III–IV) and whether God’s decree is to save believers who persevere (Article I) or a certain number of persons chosen in Christ (First Head) [[schaff3]].'],
       reformed=['For the Dutch Reformed churches and the Christian Reformed Church, the Canons, with the Belgic Confession and the Heidelberg Catechism, remain the basis of doctrine [[b_dort]]. They hold together the infinite worth of Christ’s death, “abundantly sufficient to expiate the sins of the whole world” (Second Head, Article 3), and its saving efficacy for the elect (Article 8) [[schaff3]].',
                 'The Canons insist that the promise of the gospel “ought to be declared and published to all nations, and to all persons promiscuously and without distinction, to whom God out of his good pleasure sends the gospel” (Second Head, Article 5) [[schaff3]].']),
    ))

OT1647="Genesis, Exodus, Leviticus, Numbers, Deuteronomy, Joshua, Judges, Ruth, I. Samuel, II. Samuel, I. Kings, II. Kings, I. Chronicles, II. Chronicles, Ezra, Nehemiah, Esther, Job, Psalms, Proverbs, Ecclesiastes, The Song of Songs, Isaiah, Jeremiah, Lamentations, Ezekiel, Daniel, Hosea, Joel, Amos, Obadiah, Jonah, Micah, Nahum, Habakkuk, Zephaniah, Haggai, Zechariah, Malachi."
NT1647="Matthew, Mark, Luke, John, The Acts of the Apostles, Paul's Epistles to the Romans, Corinthians I, Corinthians II, Galatians, Ephesians, Philippians, Colossians, Thessalonians I, Thessalonians II, To Timothy I, To Timothy II, To Titus, To Philemon, The Epistle to the Hebrews, The Epistle of James, The First and Second Epistles of Peter, The First, Second, and Third Epistles of John, The Epistle of Jude, The Revelation."
def wcf():
    ws=load('wcf'); items=[]; tocs=[]
    for i,x in enumerate(ws,1):
        paras=list(x['paras'])
        if i==1:
            j=[k for k,p in enumerate(paras) if p.startswith('II.')][0]
            paras[j+1:j+1]=['##Of the Old Testament',OT1647,'##Of the New Testament',NT1647]
        note=''
        if x.get('notes'):
            nt=' '.join(esc(n) for n in x['notes'] if not n.startswith('The above section'))
            note='<strong>American revision.</strong> '+('Section III is changed in the American revision, adapted to the separation of church and state, as follows: ' if i==23 else 'The American revision here adds: ')+nt+' [[schaff3]]'
        refs=[c for c in (ccel(tuple(c)) for c in x['cites']) if c]
        items.append(card(x['key'],f'Chapter {i}',esc(x['title']).replace("'","’"),paras,chips_from(refs,3),note))
        tocs.append((x['key'],f'{i}. '+esc(x['title']).replace("'","’")))
    return build(dict(slug='westminster-confession',title='The Westminster Confession of Faith (1646)',desc='The Westminster Confession of Faith in full, from the 1647 Edinburgh printing as given by Philip Schaff, with the American revisions noted, history, Scripture links, and where both traditions stand.',
     eyebrow='Reformed Confession',h1='The Westminster Confession of Faith',sub='Thirty-three chapters from the Westminster Assembly, the doctrinal standard of Presbyterian churches.',
     meta=['Westminster Assembly, 1646','Text: Edinburgh, 1647, via Schaff, 1877'],pill='Public domain',
     background=['The Westminster Assembly was called by the Long Parliament in 1643, during the English Civil War. It completed the Confession in 1646. The Church of Scotland adopted it in 1647, and the English Parliament approved a revised form in June 1648. Its thirty-three chapters follow the pattern of the Irish Articles of 1615 [[b_wcf]].',
      'Britannica calls it the “confession of faith of English-speaking Presbyterians”; some Congregationalists and Baptists also adopted it with modifications [[b_wcf]]. American Presbyterians revised the chapters on the civil magistrate and on synods to fit the separation of church and state [[schaff3]].'],
     version='The English text printed by Philip Schaff in <em>The Creeds of Christendom</em>, vol. 3 (1877), from the Edinburgh printing of 1647, with spelling and punctuation modernized by Schaff [[schaff3]]. Schaff inserts the American revisions of Chapters 23 and 31; they are shown below those chapters. His footnotes on minor American changes are not reproduced. Scripture links are drawn from the Confession’s own proof texts, up to three per chapter; the book list in Chapter 1 is laid out as running text.',
     toc=toc(tocs), items=items,
     both=dict(intro='The Confession is the classic statement of Reformed theology in English. Much of it is shared Protestant ground; the differences with Arminian theology gather in Chapters 3 (God’s decree), 9–10 (free will and effectual calling) and 17 (perseverance).',
       arminian=['Arminian churches confess with Chapter 9 that fallen man “hath wholly lost all ability of will to any spiritual good accompanying salvation” on his own; the Methodist Articles say the same of man “without the grace of God by Christ preventing us” [[schaff3]]. They differ from Chapter 3’s decree that some are “foreordained to everlasting death,” and from Chapter 17’s teaching that the effectually called “can neither totally nor finally fall away”; the Free Will Baptist confession, for example, holds that believers’ “future obedience and final salvation are neither determined nor certain” [[schaff3]].'],
       reformed=['Chapter 3 holds together God’s ordaining “whatsoever comes to pass” and the qualification that “neither is God the author of sin, nor is violence offered to the will of the creatures, nor is the liberty or contingency of second causes taken away, but rather established” [[schaff3]]. Chapter 17 grounds perseverance not in the believer’s free will but in “the immutability of the decree of election” and the work of Christ and the Spirit [[schaff3]].']),
    ))
def chips_from(refs,n):
    out=[];seen=set()
    for h,l in refs:
        pg=h.split('#')[0]
        if pg in seen: continue
        seen.add(pg); out.append((h,l))
        if len(out)>=n: break
    return out

def lbcf():
    ls=load('lbcf'); items=[]; tocs=[]
    from lib import roman as rn
    for i,x in enumerate(ls,1):
        m=re.match(r'CHAP\. ?([\dIVXL]+)\. (.*)',x['head'])
        t=m.group(2).rstrip('.').replace("Gods","God’s").replace("Lords","Lord’s")
        refs=[c for n in x['notes'] for c in parse(n)]
        items.append(card(x['key'],f'Chapter {i}',esc(t),x['paras'],chips(refs,3)))
        tocs.append((x['key'],f'{i}. {esc(t)}'))
    return build(dict(slug='second-london-baptist-confession',title='The Second London Baptist Confession (1677/1689)',desc='The Second London Baptist Confession of Faith in full, from the first printing of 1677, with history, Scripture links, and where Arminian and Reformed churches stand.',
     eyebrow='Reformed Baptist Confession',h1='The Second London Baptist Confession',sub='The Particular Baptists’ confession of 1677, owned by their General Assembly in 1689, closely following the Westminster Confession.',
     meta=['London, 1677; owned 1689','Text: first printing, 1677'],pill='Public domain',
     background=['The confession was first published in London in 1677 by Particular (Calvinistic) Baptists. It follows the Westminster Confession closely, by way of the Congregationalist Savoy Declaration of 1658, while differing on the church and on baptism [[schaff3]] [[wiki_1689]]. After the Act of Toleration of 1689, messengers from more than a hundred Particular Baptist churches met in London and approved it, which is why it is commonly called the 1689 Confession [[wiki_1689]] [[dbts_pba]].',
      'In America the Philadelphia Baptist Association adopted it in 1742 with two added articles, on the singing of psalms and the laying on of hands, as the Philadelphia Confession [[wiki_1689]] [[dbts_pba]]. Schaff printed only part of it [[schaff3]]; the full text here comes from the first edition.'],
     version='Transcribed from a copy of the first printing (London, 1677) by the Text Creation Partnership and released into the public domain [[tcp_lbcf]]. Original spelling and capitals are kept, with the long “s” modernized; a bullet (•) marks a letter the transcribers could not read. The preface and the appendix on baptism are not included. Scripture links are drawn from the confession’s own marginal proof texts, up to three per chapter.',
     toc=toc(tocs), items=items,
     both=dict(intro='The confession is Reformed in its doctrine of salvation and Baptist in its doctrine of the church. On election and grace it stands with Westminster; on the church and baptism it parts from it.',
       arminian=['Arminian Baptists such as the Free Will Baptists share this confession’s teaching that baptism is for believers and is properly by immersion (Chapter 29) [[tcp_lbcf]] [[schaff3]]. They differ from its Chapter 3 on God’s decree and Chapter 17 on perseverance; the Free Will Baptist confession, for example, says salvation is “rendered equally possible to all” [[schaff3]].'],
       reformed=['Chapter 3 is softer in one phrase than Westminster’s: where Westminster says some are “foreordained to everlasting death,” this confession says others are “left to act in their sin to their just condemnation” [[schaff3]] [[tcp_lbcf]]. Chapter 20, “Of the Gospel, and of the extent of the Grace thereof,” has no counterpart in Westminster [[tcp_lbcf]].']),
    ))

if __name__=='__main__':
    import sys
    for n in sys.argv[1:]: print(n, globals()[n]())
