import java.util.Date;

public class Apartment extends House {
    private short floorNumber;

    public Apartment(Person owner, long registrationNumber, long zoneCode, float size, short numOfRooms, short numOfFloors, Date constructionDate, short floorNumber) {
        super(owner, registrationNumber, zoneCode, size, numOfRooms, numOfFloors, constructionDate);
        this.floorNumber = floorNumber;
    }

    public String typeOfRE(){
        return "apartment";
    }

    @Override
    public float getPrice() {
        float basePrice = super.getPrice();
        if (floorNumber == 1 || floorNumber == getNumOfFloors()) {
            basePrice *= 1.05;
        }
        return basePrice;
    }

    public short getFloorNumber() {
        return floorNumber;
    }
}
