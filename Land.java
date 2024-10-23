public class Land extends RealEstate {
    public Land(Person owner, long registrationNumber, long zoneCode, float size) {
        super(owner, registrationNumber, zoneCode, size);
    }

    @Override
    protected float calculatePricePerMeter() {
        return Prices.getPricePerZone(zoneCode, Prices.landPricePerZipCode);
    }
    public String typeOfRE(){
        return "land";
    }
    @Override
    public float getPrice() {
        return pricePerMeterSqr * size;
    }
}
