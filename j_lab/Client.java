package lab1;

import java.net.*;
import java.io.*;


public class Client extends Thread {
    private static InetAddress address;
    private static MulticastSocket socket;
    private int PORT_UDP;
    private int PORT_TCP;
    private String ADDRESS;
    private String HOST;

    private Client (String HOST, String ADDRESS, int PORT_UDP, int PORT_TCP){

        this.PORT_UDP = PORT_UDP;
        this.PORT_TCP = PORT_TCP;
        this.ADDRESS = ADDRESS;
        this.HOST = HOST;
        start();
        tcp_transmit();
    }

    public void tcp_transmit (){
        //System.out.println("tcp_transmit") ;
        InputStreamReader inp=new InputStreamReader(System.in);
        BufferedReader br=new BufferedReader(inp);
        try {
            Socket clientSocket = new Socket(HOST, PORT_TCP);
            OutputStream sout = clientSocket.getOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(sout);
            System.out.println("Enter your nick name: ");
            String nickname = br.readLine();
            while (true){
                clientMessage cm = new clientMessage();
                cm.setName(nickname);
                System.out.println("Enter message ");
                String str = br.readLine();
                cm.setMessage(str);
                oos.writeObject(cm);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void run(){
        try {
            socket = new MulticastSocket(PORT_UDP);
            address = InetAddress.getByName(ADDRESS);
            socket.joinGroup(address);
            String str;
            byte[] buffer;
            DatagramPacket packet;
            while (true) {
                buffer = new byte[256];
                packet = new DatagramPacket(
                        buffer, buffer.length);
                socket.receive(packet);
                str = new String(packet.getData());
                System.out.println(str.trim());
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                socket.leaveGroup(address);
                socket.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] ar) {
        int PORT_UPD = 1502;
        int PORT_TCP = 1500;
        String HOST = "127.0.0.1";
        String ADDRESS = "233.0.0.1";
        new Client(HOST, ADDRESS, PORT_UPD, PORT_TCP);
    }
}