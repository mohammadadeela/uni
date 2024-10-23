import java.util.ArrayList;

public class Building extends RealEstate {
    private ArrayList<Apartment> apartments;

    public Building(Person owner, long registrationNumber, long zoneCode) {
        super(owner, registrationNumber, zoneCode, 0);
        this.apartments = new ArrayList<>();
    }

    public void addApartment(Apartment apartment) {
        apartments.add(apartment);
    }

    public ArrayList<Apartment> getApartments() {
        return apartments;
    }

    public String typeOfRE(){
        return "building";
    }
    @Override
    protected float calculatePricePerMeter() {
        return Prices.getPricePerZone(zoneCode, Prices.buildingPricePerZipCode);
    }

    @Override
    public float getPrice() {
        float totalPrice = 0;
        for (Apartment apartment : apartments) {
            totalPrice += apartment.getPrice();
        }
        return totalPrice;
    }
}
