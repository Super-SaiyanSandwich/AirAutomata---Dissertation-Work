import javax.script.*;
import java.io.*;

public class test {
    public static void main(String[] args) throws Exception {
        System.out.println("::TEST::");

        ScriptEngine engine = new ScriptEngineManager().getEngineByName("nashorn");
        engine.eval(new FileReader("script.js"));
        
        Invocable invocable = (Invocable) engine;     

        Object ATOMresult = invocable.invokeFunction("ATOMread", "http://uk-air.defra.gov.uk/data/atom-dls/auto/2018/GB_FixedObservations_2018_ABD.atom.en.xml");
 
        System.out.println(ATOMresult);
    }
}