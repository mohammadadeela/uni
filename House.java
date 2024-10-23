import java.util.Date;

public class House extends RealEstate {
    private short numOfRooms;
    private short numOfFloors;
    private Date constructionDate;

    public House(Person owner, long registrationNumber, long zoneCode, float size, short numOfRooms, short numOfFloors, Date constructionDate) {
        super(owner, registrationNumber, zoneCode, size);
        this.numOfRooms = numOfRooms;
        this.numOfFloors = numOfFloors;
        this.constructionDate = constructionDate;
    }

    @Override
    protected float calculatePricePerMeter() {
        return Prices.getPricePerZone(zoneCode, Prices.housePricePerZipCode);
    }

    public short getNumOfFloors() {
        return numOfFloors;
    }

    @Override
    public float getPrice() {
        float basePrice = pricePerMeterSqr * size;
        if (numOfFloors > 1) {
            basePrice *= 0.8;
        }
        long age = (new Date().getTime() - constructionDate.getTime()) / (1000L * 60 * 60 * 24 * 365);
        if (age > 35) {
            basePrice *= 0.5;
        }
        return basePrice;
    }

    public String typeOfRE(){
        return "hosue";
    }

    public short getNumOfRooms() {
        return numOfRooms;
    }

    public Date getConstructionDate() {
        return constructionDate;
    }
}
