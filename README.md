Modern-Mudfare
==============

My first MUD

package modernmudfare;
import java.util.Scanner;  // scanner method is used to recieve input from user
public class ModernMudfare {
    
// main method that is executed 
    public static void main(String[] args) {
        // Declaration of Varibalies to be called in the main method
        Boolean InCombat;
        Boolean gameover;
        int input;
        String currentLocation;
        Player Player1 = new Player();
        Location PLocation = new Location();
        Scanner keyboardInput = new Scanner (System.in);
        gameover = false;
        System.out.println("Welcome to Modern Mudfare!");
        System.out.println("You spawned in the "+ PLocation.startlocation()+"!");
        while (!gameover){
           // start of game and each step from the player reminds them of their
            //status
            System.out.println("You have " +Player1.GetHealth()+  " health");
            System.out.println("You have " +Player1.GetStamina()+  " stamina");
            System.out.println("You have " +Player1.GetStrength()+  " strength");
            System.out.println("You have " +Player1.GetMana()+  " mana");
            
            //current choices of the player
            System.out.println("What would you like to do? ");   
            System.out.println("1 = Walk, 2 = Stay");
            System.out.print("> ");
            input = keyboardInput.nextInt();
        if (Player1.GetStamina()  >= 10)
        {   // if else statements are used to cycle thru the sequence of events
            //between the player and the world
            if (input == 1) {
                System.out.println("You have taken a few steps forward ");
                System.out.println("You are now in the " + PLocation.NextLocation() + "!");
                System.out.println("You have lost 10 points of stamina");
                Player1.loseStamina(10);
                    }
        }
        else{
            System.out.println("You do not have enough stamina, you must rest to replenish");
            System.out.println("You have stopped to rest, \nYou rest and regain 20 stamina");
            Player1.regainStamina(20);
        }
        if (input ==2){
            System.out.println("You have stopped to rest, \nYou rest and regain 20 stamina");
            Player1.regainStamina(20);
        }
        
        
        
            
            
            
    }
    
    
    }
    
    
}

package modernmudfare;

/** public class Combat {
    final int chanceOfDrop = 3;
    static Weapons[] wepArray = {new M4(), new M16()}
    static boolean[] hasWeapon = {false, true};

    public static int  ranNumberGen(int chanceOfDrop) {
        return (int) (Math.random()*1); 
    }

    private void enemyDead() {
        boolean canDrop = false;
        if(ranNumberGen(chanceOfDrop)==0){
            canDrop = true;

        }

        if(canDrop == true){
            givePlayerWeapon(Weapon[Combat.ranNumberGen(Weapons.length)]);
        }

        private static void givePlayerWeapon(int w) {
            hasWeapon[w] = true;

            for w <(Weapons.length-1) {
                if has weapon[w] {
                    System.out.println(wepArray[w].getWeaponName);
                }
                }
        }
    }

    }
}
 *
 * 
 */
public class Combat {
    
}
/* 
public abstract class M4 {
  private Integer weaponDamage = 5;
  private Integer weaponAmmo = 25;
  private String weaponName = "M4";

  public M4(String name, int ammo, int damage) {
    name = weaponName;
    ammo = weaponAmmo;
    damage = weaponDamage;
  }

  public String getWeaponName() {
    return weaponName;
  }

  public Integer getAmmo() {
    return weaponAmmo;
  }

  public Integer getDamage() {
    return weaponDamage;
  }
}
*/

/*Another Syntax I think may work I got from a friend is:  
 You have to think about when it fires, first. Options:
1. Time interval (e.g. every 2 seconds, fired off via timer)
2. Per frame (e.g. in your update() function)
3. Per distance travelled (e.g., in update(), have a counter that increments every time the character takes a step)

Once you do one of the above (e.g. every 5 steps), you need to execute code that's something like this:

int percentChance = rand() % 100 + 1; // range 1-100
if(percentChance <= 30) { // 30% chance to do combat every 5 steps
doCombat();
}


*/

// the location class. Contains the stages to be used in the main method
package modernmudfare;
import java.util.Random;

public class Location {
    Random PLocation = new Random(); 
    private String _location;
public String startlocation(){
    int Slocate = PLocation.nextInt((3-1)+1)+1; 
        if (Slocate == 1)
            _location = "Forest";
        if (Slocate == 2)
            _location = "Desert";
        if (Slocate == 3)
            _location = "Sewer";
             return _location;
}   // random generator to randomly change the stage when you take steps.
public String NextLocation(){
    int NLocate = PLocation.nextInt((3-1)+1)+1;
        if (NLocate == 1)
            _location = "Forest";
        if (NLocate == 2)            
            _location = "Desert";
        if (NLocate == 3)
            _location = "Sewer";
            return _location;
}
    
    
    
}

package modernmudfare;

// a class for the ogre monster and its variables to be called into the main 
//method
public class Ogre {

    private int _health = 60;
    private int _strength = 8;
            
public int GetHealth(){
    return _health;
}

public int GetStrength(){
    return _strength; 
}
}

package modernmudfare;

// player class.  Contains all vairables to be called into the main method for 
// the player
public class Player {
    private int _health = 100;
    private int _stamina = 50;
    private int _strength = 50;
    private int _mana = 100;
       
    public int GetHealth(){
        return _health;
    }
               
    public int GetStamina(){
        return _stamina;
    }
    public int GetStrength(){
        return _strength;
    }
    public int GetMana(){
        return _mana;
    }
    public void loseStamina(int x){
        _stamina = _stamina - x;
    }
    public void regainStamina(int x) {
        _stamina = _stamina + x;
        if (_stamina > 50) 
            _stamina = 50;
    }
}




package modernmudfare;

// A class for the troll monster and its variables to be called into the main
//method
public class Troll {
    
private int _health = 60;
private int _strength = 7;

public int GetHealth(){
    return _health;
}
public int GetStrength(){
    return _strength;
}
}

package modernmudfare;

// A class for the Wolf monster and its variables to be called into the main
//method
public class Wolf {

    private int _health = 50;
    private int _strength = 5;
    
public int GetHealth(){
    return _health;
}

public int GetStrength(){
    return _strength;
}
}
