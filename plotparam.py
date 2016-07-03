from ROOT import *


pmt0 = [ 0.00057463350052676570, 1.1198342880594443e-06,
        -9.3561602528855980e-08, 3.5120362369139496e-09,
        -7.4440362446034840e-11, 9.3317901914795150e-13,
        -7.0803511879738476e-15, 3.1831360164201030e-17,
        -7.7761552084330930e-20, 7.9080464114437250e-23]

pmt1 = [ 0.00057710608427653220, 8.472667988561730e-07,
        -8.0629763245973410e-08, 3.152313344688961e-09,
        -6.8080980196578850e-11, 8.611299097069648e-13,
        -6.5656763435765475e-15, 2.960562658312417e-17,
        -7.2462358110856350e-20, 7.376294944669138e-23]

pmt2 = [ 0.0005780642361101156, 8.1906122465485610e-07,
        -8.277333123588723e-08, 3.3343076430888800e-09,
        -7.341698427903352e-11, 9.4152013979943200e-13,
        -7.252514847355433e-15, 3.2966111312086194e-17,
        -8.123596144731072e-20, 8.3237857519052030e-23]

pmt3 = [ 0.00049535395820990410, -8.9446898316894650e-07,
         5.9543798557352650e-08, -2.1442979394850743e-09,
         4.2903482120385170e-11, -5.2091173192216000e-13,
         3.9040136983565505e-15, -1.7683630173256570e-17,
         4.4485141691909330e-20, -4.7957677994189266e-23]

pmt4 = [ 0.00049174919407915180, -3.9827831247602750e-07,                                                       3.2969430404548925e-08, -1.3976901905215522e-09,                                                     3.0465890151072795e-11, -3.9105217577978583e-13,                                                         3.0435806386397590e-15, -1.4168565261192278e-17,                                                             3.6415138604698307e-20, -4.0001444619145063e-23]

pmt5 = [ 0.00049247158889589830, -5.8331484805604160e-07,                                                                             4.4745424221348430e-08, -1.7458627974514014e-09,                                                                                 3.6185693067669710e-11, -4.4738029368364670e-13,                                                                                     3.3835276194585322e-15, -1.5397970137699067e-17,                                                                                         3.8855134323223576e-20, -4.2038323991921250e-23]

pmt6 = [ 0.00048984991992208060,  3.1900366858745684e-08,                                                                                                         2.1793082366859870e-09, -3.3620306175021700e-10,                                                                                                             1.0074612783020127e-11, -1.5703674431733906e-13,                                                                                                                 1.4001643875422070e-15, -7.2397072908273930e-18,                                                                                                                     2.0300474694556284e-20, -2.4104180621705204e-23]

pmt7 = [ 0.00049203663047765460, -3.6488508324640986e-07,                                                                                                                                     2.6481244920799626e-08, -1.0533015661054176e-09,                                                                                                                                         2.1874295810917937e-11, -2.7284817624770730e-13,                                                                                                                                             2.0933154494194566e-15, -9.7198150571751580e-18,                                                                                                                                                 2.5175167876548474e-20, -2.8153861835545850e-23]

pmt8 = [ 0.00048977000081774430, -3.1311942225551570e-08,                                                                                                                                                                 1.0677456178060788e-08, -7.4776905495254960e-10,                                                                                                                                                                     1.9681662516071090e-11, -2.8118378006946710e-13,                                                                                                                                                                         2.3407909518291974e-15, -1.1410437093914491e-17,                                                                                                                                                                             3.0337898868205930e-20, -3.4240190444743415e-23]

pmt9 = [ 0.0004931028882493679, -5.3906664493416560e-07,                                                                                                                                                                                             4.031094256980346e-08, -1.6230579718189475e-09,                                                                                                                                                                                                 3.460555365504150e-11, -4.3688736695545270e-13,                                                                                                                                                                                                     3.348332888086907e-15, -1.5347041247701560e-17,                                                                                                                                                                                                         3.883030901098478e-20, -4.1998848485133410e-23]

pmt10 = [ 0.00049231866920777800, -4.1049198186780320e-07,                                                                                                                                                                                                                         2.9333372641866090e-08, -1.1519111146254383e-09,                                                                                                                                                                                                                             2.3863152386034654e-11, -2.9740440205352990e-13,                                                                                                                                                                                                                                 2.2807328728662075e-15, -1.0578551788609108e-17,                                                                                                                                                                                                                                     2.7333577871282617e-20, -3.0437190417900910e-23]

pmt11 = [ 0.00048920561013751100,  7.6199978948473570e-08,                                                                                                                                                                                                                                                     2.0087870268194676e-09, -4.1043772158172164e-10,                                                                                                                                                                                                                                                         1.2567426427434073e-11, -1.9402050435291178e-13,                                                                                                                                                                                                                                                             1.7015978856781205e-15, -8.6431219142754850e-18,                                                                                                                                                                                                                                                                 2.3813411850158440e-20, -2.7781173812464524e-23]

time0 = [ 7.72722805362115e-05  , -1.7324838006211257e-07,                                                                                                                                                                                                                                                                                     -1.5187346606435122e-06, -2.5091835257793633e-07,                                                                                                                                                                                                                                                                                         1.1253294758937517e-07, -1.4959187625910396e-08,                                                                                                                                                                                                                                                                                             1.0478364509355833e-09, -4.1983487389956764e-11,                                                                                                                                                                                                                                                                                                 9.138336643671175e-13 , -8.417934001312287e-15 ]

time1 = [ 0.00011677571226478973,  3.0681114251758713e-06,                                                                                                                                                                                                                                                                                                                 -7.020228451072785e-06 ,  6.580231019104729e-07 ,                                                                                                                                                                                                                                                                                                                     8.875235171384665e-08 , -2.2630647945150987e-08,                                                                                                                                                                                                                                                                                                                         2.001407767777557e-09 , -9.1941087597627e-11   ,                                                                                                                                                                                                                                                                                                                             2.1995529129997883e-12, -2.1738264013652286e-14 ]


pmts   = [ pmt0, pmt1, pmt2, pmt3, pmt4, pmt5, pmt6, pmt7, pmt8, pmt9, pmt10, pmt11 ]
times  = [ time0, time1 ]
colors = [ kRed, kBlack, kBlue, kOrange, kGreen, kCyan, kGray, kMagenta, kViolet, kAzure, kYellow ]
npmts  = len(pmts)
ntimes = len(times)
poly   = ' + '.join( [ '[{0}]*x^{0}'.format(i) for i in range(10) ] )
PMTf   = [ TF1( 'PMT' +str(i), poly, 0, 225 ) for i in range(npmts) ]
SiPMf  = [ TF1( 'time'+str(i), poly, 0, 21 ) for i in range(ntimes) ]
[ f.SetParameters(*p) for f,p in zip(PMTf,pmts) ]
[ f.SetParameters(*p) for f,p in zip(SiPMf,times) ]
[ f.SetLineColor(c) for f,c in zip(PMTf,colors) ]
[ f.SetLineColor(c) for f,c in zip(SiPMf,colors) ]
#map( TF1.SetLineColor, PMTf, colors )
#map( TF1.SetLineColor, SiPMf, colors )
'''
PMTcanvas = TCanvas()
PMTf[0].Draw()
[ f.Draw('same') for f in PMTf[1:] ]
SiPMcanvas = TCanvas()
SiPMf[-1].Draw()
[ f.Draw('same') for f in reversed(SiPMf[:-1]) ]
raw_input('done')
'''

