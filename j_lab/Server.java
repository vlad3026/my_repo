package lab1;
import java.net.*;
import java.io.*;
import java.util.Timer;
import java.util.TimerTask;
import java.util.Vector;
import java.util.Iterator;
import java.util.concurrent.Semaphore;


class tcpClientThread extends Thread {
    private Socket clSocket;
    static Semaphore semaphore = new Semaphore(1);
    public static Vector<clientMessage> vec = new Vector<>();
    public tcpClientThread(Socket clSocket)  {
        this.clSocket = clSocket;
    }


    public void run ()  {
        try {
            ObjectInputStream oin = new ObjectInputStream(clSocket.getInputStream());
            while (true){
                clientMessage cm = (clientMessage) oin.readObject();
                semaphore.acquire();
                System.out.println(cm.getName()+": "+cm.getMessage()) ; // -----------------------------------//
                vec.addElement(cm);
                semaphore.release();
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
}


public class Server  {
    private String str = null;
    private byte[] buffer;
    private DatagramPacket packet;
    private InetAddress address;
    private DatagramSocket socket;
    private int PORT_UDP;
    private int PORT_TCP;
    private String ADDRESS;


    private Server(String ADDRESS, int PORT_UDP, int PORT_TCP){
        System.out.println("Server started!");
        this.PORT_UDP = PORT_UDP;
        this.PORT_TCP = PORT_TCP;
        this.ADDRESS = ADDRESS;
        udp_transmit();
        tcp_transmit();
    }
    private void tcp_transmit(){
        try {
            ServerSocket server = new ServerSocket(PORT_TCP);
            while (true) {
                Socket clientSocket = server.accept();
                System.out.println("Connection accepted: " +clientSocket.getInetAddress().getHostAddress());
                tcpClientThread ct = new tcpClientThread(clientSocket);
                ct.start();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void udp_transmit()
    {
        final Timer time = new Timer();
        try {
            socket = new DatagramSocket();
        } catch (Exception e) {
            e.printStackTrace();
        }
        time.schedule(new TimerTask() {
            @Override
            public void run() {
                try {
                        tcpClientThread.semaphore.acquire();
                        for (Iterator<clientMessage> iter = tcpClientThread.vec.iterator(); iter.hasNext();){
                            clientMessage cm =iter.next();
                            str = cm.getName() + ": " + cm.getMessage();
                            buffer = str.getBytes();
                            address = InetAddress.getByName(ADDRESS);
                            packet = new DatagramPacket(
                                    buffer,
                                    buffer.length,
                                    address,
                                    PORT_UDP);
                            socket.send(packet);
                            iter.remove();

                        }
                        tcpClientThread.semaphore.release();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }, 1000, 10000);

    }

    public static void main(String[] ar)    {
        int PORT_UPD = 1502;
        int PORT_TCP = 1500;
        String ADDRESS = "233.0.0.1";
        new Server(ADDRESS, PORT_UPD, PORT_TCP);
    }
}