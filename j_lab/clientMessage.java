package lab1;

import java.io.Serializable;

public class clientMessage implements Serializable {

    private String nickName;
    private String message;

    public clientMessage(){
        this.nickName = "unnamed";
        this.message = "";
    }
    public void setName (String name){
        this.nickName = name;
    }

    public void setMessage (String message){
        this.message = message;
    }

    String getName (){
        return this.nickName;
    }

    String getMessage (){
        return this.message;
    }
}
