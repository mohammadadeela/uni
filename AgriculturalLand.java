public class AgriculturalLand extends Land {
    public AgriculturalLand(Person owner, long registrationNumber, long zoneCode, float size) {
        super(owner, registrationNumber, zoneCode, size);
    }

    @Override
    protected float calculatePricePerMeter() {
        return Prices.getPricePerZone(zoneCode, Prices.agriLandPricePerZipCode);
    }

    public String typeOfRE(){
        return "agricultral land";
    }

    @Override
    public float getPrice() {
        return pricePerMeterSqr * size;
    }
}
