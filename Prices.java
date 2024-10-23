import java.util.ArrayList;

public class Prices {
    public static ArrayList<Long> zoneCodes = new ArrayList<>();
    public static ArrayList<Float> housePricePerZipCode = new ArrayList<>();
    public static ArrayList<Float> buildingPricePerZipCode = new ArrayList<>();
    public static ArrayList<Float> landPricePerZipCode = new ArrayList<>();
    public static ArrayList<Float> agriLandPricePerZipCode = new ArrayList<>();

    public static float getPricePerZone(long zoneCode, ArrayList<Float> priceList) {
        int index = zoneCodes.indexOf(zoneCode);
        if (index != -1) {
            return priceList.get(index);
        }
        return 0;
    }

    // method to load prices based on specifi zone codes
    public static void loadPrices() {
        zoneCodes.add(101L); housePricePerZipCode.add(1500f); buildingPricePerZipCode.add(1400f); landPricePerZipCode.add(800f); agriLandPricePerZipCode.add(600f);
        zoneCodes.add(102L); housePricePerZipCode.add(1600f); buildingPricePerZipCode.add(1500f); landPricePerZipCode.add(900f); agriLandPricePerZipCode.add(700f);
        zoneCodes.add(103L); housePricePerZipCode.add(1700f); buildingPricePerZipCode.add(1600f); landPricePerZipCode.add(1000f); agriLandPricePerZipCode.add(800f);
    }
}
