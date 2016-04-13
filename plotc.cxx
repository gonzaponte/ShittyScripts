#include <cmath>
#include <string>
#include <iostream>
#include <gmp.h>

#include "TCanvas.h"
#include "TH2F.h"
#include "TROOT.h"


mpz_t _17,_2,_1;
bool DEBUG = false;

int f( mpz_t x, mpz_t y )
{
    mpz_t xx, yy, yyy;
    mpz_init( xx ); mpz_init( yy ); mpz_init( yyy );
    
    if (DEBUG) std::cout << "x " << mpz_get_ui(x) << " y " << mpz_get_ui(y) << std::endl;

    mpz_mul   (  xx,  x, _17 );    if (DEBUG) std::cout << "2 " << mpz_get_ui(xx) << std::endl;

    mpz_fdiv_r(  yy,  y, _17 );    if (DEBUG) std::cout << "3 " << mpz_get_ui(yy) << std::endl;

    mpz_fdiv_q( yyy,  y, _17 );    if (DEBUG) std::cout << "4 " << mpz_get_ui(yyy) << std::endl;

    mpz_add   (  xx, xx,  yy );    if (DEBUG) std::cout << "5 " << mpz_get_ui(xx) << std::endl;
    
    mpz_powm( xx, _2, xx, _1);    if (DEBUG) std::cout << "6 " << mpz_get_ui(xx) << std::endl;

    mpz_fdiv_q( xx, yyy, xx );    if (DEBUG) std::cout << "7 " << mpz_get_ui(xx) << std::endl;

    mpz_fdiv_r( xx, xx, _2 );    if (DEBUG) std::cout << "8 " << mpz_get_ui(xx) << std::endl;

    bool result = 1UL < 2UL * mpz_get_ui( xx );
    return (int) result;
}

int main(void)
{
    mpz_init_set_ui( _17, 17UL );
    mpz_init_set_ui( _2 ,  2UL );
    mpz_init_set_ui( _1 , 10000UL );

    mpz_t k;
//    mpz_init_set_str( k, "50003018008", 10);
    mpz_init_set_str( k,"960939379918958884971672962127852754715004339660129306651505519271702802395266424689642842174350718121267153782770623355993237280874144307891325963941337723487857735749823926629715517173716995165232890538221612403238855866184013235585136048828693337902491454229288667081096184496091705183454067827731551705405381627380967602565625016981482083418783163849115590225610003652351370343874461848378737238198224849863465033159410054974700593138339226497249461751545728366702369745461014655997933798537483143786841806593422227898388722980000748404719", 10 );
//    mpz_init_set_str( k,"4858450636189713423582095962494202044581400587983244549483093085061934704708809928450644769865524364849997247024915119110411605739177407856919754326571855442057210445735883681829823754139634338225199452191651284348332905131193199953502413758765239264874613394906870130562295813219481113685339535565290850023875092856892694555974281546386510730049106723058933586052544096664351265349363643957125565695936815184334857605266940161251266951421550539554519153785457525756590740540157929001765967965480064427829131488548259914721248506352686630476300", 10 );

    TH2F h = TH2F("h",std::to_string(mpz_get_ui(k)).c_str(),106,0,106,3*17,0,3*17);
    
    for ( unsigned long int x = 0UL; x<106UL; ++x)
    {
//        std::cout << x << " ";
        mpz_t x_mp; mpz_init_set_ui( x_mp, x );
        
        for ( unsigned long int y = 0UL ; y<17UL; ++y)
        {
            mpz_t y_mp; mpz_init_set_ui( y_mp, y );
            mpz_t k_plus_mp; mpz_init( k_plus_mp ); mpz_add( k_plus_mp, k, y_mp );
            h.SetBinContent( h.GetBin( x+1, 35-y ), f(x_mp,k_plus_mp) );
        }
    }
    TCanvas* c = new TCanvas();
    h.Draw("zcol");
    c->Update();
    c->SaveAs("plt.pdf");
    int a;
    std::cout << "Listo!" << std::endl;
    //std::cin >> a;
    return 0;
}

//
//g++ -o plotc plotc.cxx -lgmp `root-config --cflags --glibs --libs`
//
