package mainPackage;
import java.io.*;
public class Main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}
	
	public static boolean overlap(String f, String s)
    {
       if(f.equals(s))
           return false;
       
       String[] f_arr = f.split(" ");
       int l1 = f_arr.length;
       String[] s_arr = s.split(" ");
       int l2 = s_arr.length;

       String str_f = "";
       String str_s = "";
       
       for(int i = 0; i < Integer.min(l1,l2); i++)
       {
           str_f = f_arr[l1-1-i] + str_f;
           str_s = str_s + s_arr[i]; 
           
           if(str_f.equals(str_s))
           {
               return true;
           }
           str_f = " "+str_f;
           str_s = str_s+" ";
       }
       return false;
    }
    
         
    public static String[] ReadList(String path) throws IOException
    {
        FileReader fr = new FileReader(path);
        BufferedReader txt = new BufferedReader(fr);
        
        String[] result = new String[6561];
        
        for(int i = 0; i <6561; i++)
        {
            result[i] = txt.readLine();
        }
        txt.close();
        fr.close();
        return result;
        
    }

}
