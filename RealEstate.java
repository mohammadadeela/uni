public abstract class RealEstate implements Comparable<RealEstate> {
    protected Person owner;

    protected long registrationNumber;
    protected long zoneCode;
    protected float pricePerMeterSqr;
    protected float size;

    public RealEstate(Person owner, long registrationNumber, long zoneCode, float size) {
        this.owner = owner;
        this.registrationNumber = registrationNumber;
        this.zoneCode = zoneCode;
        this.size = size;
        this.pricePerMeterSqr = calculatePricePerMeter();
    }

    public long getRegistrationNumber() {
        return registrationNumber;
    }

    protected abstract float calculatePricePerMeter();

    public abstract String typeOfRE();

    public abstract float getPrice();

    public int compareTo(RealEstate other) {
        return Float.compare(this.getPrice(), other.getPrice());
    }

    public boolean equalsTo(RealEstate other) {
        return this.registrationNumber == other.registrationNumber;
    }

    @Override
    public String toString() {
        return "real estate type: " + typeOfRE() + ", Registration Number: " +
                registrationNumber + ", Owner: " + owner.getName() +
                ", Zone Code: " + zoneCode + ", Size: " + size + "sq meters, Price: $" + getPrice();
    }
}
