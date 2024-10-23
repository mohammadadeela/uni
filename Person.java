import java.util.ArrayList;

public class Person {
    private String name;
    private long ID;
    private ArrayList<RealEstate> properties;

    public Person(String name, long ID) {
        this.name = name;
        this.ID = ID;
        this.properties = new ArrayList<>();
    }

    public String getName() {
        return name;
    }

    public long getID() {
        return ID;
    }

    public ArrayList<RealEstate> getProperties() {
        return properties;
    }

    public void addProperty(RealEstate property) {
        properties.add(property);
    }
}
