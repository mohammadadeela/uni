import java.io.*;
import java.util.*;

public class RealEstateApp {

    private static ArrayList<Person> persons = new ArrayList<>();

    public static void main(String[] args) {
        Prices.loadPrices();
        loadFromFile();
        Scanner scanner = new Scanner(System.in);

        // display menu
        while (true) {
            System.out.println("1. insert a new person");
            System.out.println("2. insert a new real estate");
            System.out.println("3. find a real estate by registeration number");
            System.out.println("4. find a certain person properties");
            System.out.println("5. terminat and save to output.txt");
            int choice = scanner.nextInt();
            scanner.nextLine();


            if (choice == 1)
                addPerson(scanner);

            else if (choice == 2)
                addRealEstate(scanner);
            else if (choice == 3)
                searchRealEstate(scanner);
            else if (choice == 4)
                searchPersonProperties(scanner);
            else if (choice == 5) {
                saveToFile();
                System.out.println("the output is stored in output.txt");
                System.exit(0);
            } else
                System.out.println("Wrong input please try again!");
        }

    }

    private static void addPerson(Scanner scanner) {
        System.out.println("please enter the first and last name (separated by a space):");
        String name = scanner.nextLine();

        // validate name format
        if (!name.contains(" ") || name.trim().split("\\s+").length != 2) {
            System.out.println("invalid name format. please enter a first and last name separated by a space.");
            return;
        }

        System.out.println("please enter a numeric id:");
        // validate id is an integer
        if (!scanner.hasNextInt()) {
            System.out.println("invalid id. please enter a valid integer id.");
            scanner.next(); // clear invalid input
            return;
        }
        int id = scanner.nextInt();

        // check if id exists
        if (findPersonById(id) != null) {
            System.out.println("this id already exists. please try again.");
            return;
        }

        persons.add(new Person(name, id));
        System.out.println("person added successfully.");
    }

    // method to add a real estate
    private static void addRealEstate(Scanner scanner) {
        System.out.println("type in person's ID:");
        long id = scanner.nextLong();
        Person person = findPersonById(id);
        if (person == null) {
            System.out.println("invalid PID");
            return;
        }

        System.out.println("choose the real estate type:\n1-House\n2-Building\n3-Land\n4-AgriculturalLand\n");
        int type = scanner.nextInt();

        if (type == 1)
            addHouse(scanner, person);
        else if (type == 2)
            addBuilding(scanner, person);
        else if (type == 3)
            addLand(scanner, person);
        else if (type == 4)
            addAgriculturalLand(scanner, person);
        else
            System.out.println("wrong input try again please!");

    }

    // method to add a house
    private static void addHouse(Scanner scanner, Person person) {
        long regNo = getValidRegistrationNumber(scanner);
        long zoneCode = getValidZoneCode(scanner);

        if (zoneCode == -1) return;

        System.out.println("enter size:");
        float size = scanner.nextFloat();
        System.out.println("enter number of rooms:");
        short numOfRooms = scanner.nextShort();
        System.out.println("enter number of floors:");
        short numOfFloors = scanner.nextShort();
        System.out.println("enter construction year:");
        int year = scanner.nextInt();
        Date constructionDate = new GregorianCalendar(year, Calendar.JANUARY, 1).getTime();

        RealEstate house = new House(person, regNo, zoneCode, size, numOfRooms, numOfFloors, constructionDate);
        person.addProperty(house);
    }

    // method to add a building
    private static void addBuilding(Scanner scanner, Person person) {
        long regNo = getValidRegistrationNumber(scanner);
        long zoneCode = getValidZoneCode(scanner);

        if (zoneCode == -1) return;

        Building building = new Building(person, regNo, zoneCode);
        person.addProperty(building);
    }

    // method to add a land
    private static void addLand(Scanner scanner, Person person) {
        long regNo = getValidRegistrationNumber(scanner);
        long zoneCode = getValidZoneCode(scanner);

        if (zoneCode == -1) return;

        System.out.println("enter size:");
        float size = scanner.nextFloat();
        RealEstate land = new Land(person, regNo, zoneCode, size);
        person.addProperty(land);
    }

    // method to add an agricultural land
    private static void addAgriculturalLand(Scanner scanner, Person person) {
        long regNo = getValidRegistrationNumber(scanner);
        long zoneCode = getValidZoneCode(scanner);

        if (zoneCode == -1) return;

        System.out.println("enter size:");
        float size = scanner.nextFloat();
        RealEstate agriLand = new AgriculturalLand(person, regNo, zoneCode, size);
        person.addProperty(agriLand);
    }

    // returns if the registeration id is valid or not
    private static long getValidRegistrationNumber(Scanner scanner) {
        System.out.println("enter registration number:");
        long regNo = scanner.nextLong();

        if (findRealEstateByRegistrationNumber(regNo) != null) {
            System.out.println("registration number already exists. please try again.");
            return getValidRegistrationNumber(scanner);
        }

        return regNo;
    }

    // checks if it is a valid zone code
    private static long getValidZoneCode(Scanner scanner) {
        System.out.println("enter zone code:");
        long zoneCode = scanner.nextLong();

        if (!Prices.zoneCodes.contains(zoneCode)) {
            System.out.println("invalid xone code. please try again.");
            return -1;
        }

        return zoneCode;
    }

    // searches for a real estate and prints the property if it exists
    private static void searchRealEstate(Scanner scanner) {
        System.out.println("enter registration number:");
        long regNo = scanner.nextLong();
        RealEstate property = findRealEstateByRegistrationNumber(regNo);

        if (property != null) {
            System.out.println(property);
        } else {
            System.out.println("real estate not found.");
        }
    }

    // searches for a person's properties based on PID and prints the propertires
    private static void searchPersonProperties(Scanner scanner) {
        System.out.println("enter person ID:");
        long id = scanner.nextLong();
        Person person = findPersonById(id);

        if (person == null) {
            System.out.println("person not found.");
            return;
        }

        for (RealEstate property : person.getProperties()) {
            System.out.println(property);
        }
    }

    // searches for a person based on ID
    private static Person findPersonById(long id) {
        for (Person person : persons) {
            if (person.getID() == id) {
                return person;
            }
        }
        return null;
    }

    // finds the reals estate by the reg number
    private static RealEstate findRealEstateByRegistrationNumber(long regNo) {
        for (Person person : persons) {
            for (RealEstate property : person.getProperties()) {
                if (property.getRegistrationNumber() == regNo) {
                    return property;
                }
            }
        }
        return null;
    }


    // loads the input data from the input file input.txt
    private static void loadFromFile() {
        ArrayList<Building> buildings = new ArrayList<Building>();
        ArrayList<Apartment> apartments = new ArrayList<Apartment>();
        try (BufferedReader br = new BufferedReader(new FileReader("input.txt"))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",");
                String type = parts[0];
                if (type.equals("Person")) {
                    String name = parts[1];
                    long id = Long.parseLong(parts[2]);
                    persons.add(new Person(name, id));
                } else if (type.equals("House")) {
                    Person owner = findPersonById(Long.parseLong(parts[1]));
                    long regNo = Long.parseLong(parts[2]);
                    long zoneCode = Long.parseLong(parts[3]);
                    float size = Float.parseFloat(parts[4]);
                    short numOfRooms = Short.parseShort(parts[5]);
                    short numOfFloors = Short.parseShort(parts[6]);
                    Date constructionDate = new GregorianCalendar(Integer.parseInt(parts[7]), Calendar.JANUARY, 1).getTime();
                    RealEstate house = new House(owner, regNo, zoneCode, size, numOfRooms, numOfFloors, constructionDate);
                    owner.addProperty(house);
                } else if (type.equals("Building")) {
                    Person owner = findPersonById(Long.parseLong(parts[1]));
                    long regNo = Long.parseLong(parts[2]);
                    long zoneCode = Long.parseLong(parts[3]);
                    Building building = new Building(owner, regNo, zoneCode);
                    owner.addProperty(building);
                    buildings.add(building);
                } else if (type.equals("Apartment")) {
                    Person owner = findPersonById(Long.parseLong(parts[1]));
                    long regNo = Long.parseLong(parts[2]);
                    long zoneCode = Long.parseLong(parts[3]);
                    float size = Float.parseFloat(parts[4]);
                    short numOfRooms = Short.parseShort(parts[5]);
                    short numOfFloors = Short.parseShort(parts[6]);
                    Date constructionDate = new GregorianCalendar(Integer.parseInt(parts[7]), Calendar.JANUARY, 1).getTime();
                    short floorNumber = Short.parseShort(parts[8]);
                    Apartment apartment = new Apartment(owner, regNo, zoneCode, size, numOfRooms, numOfFloors, constructionDate, floorNumber);
                    owner.addProperty(apartment);
                    apartments.add(apartment);
                } else if (type.equals("Land")) {
                    Person owner = findPersonById(Long.parseLong(parts[1]));
                    long regNo = Long.parseLong(parts[2]);
                    long zoneCode = Long.parseLong(parts[3]);
                    float size = Float.parseFloat(parts[4]);
                    RealEstate land = new Land(owner, regNo, zoneCode, size);
                    owner.addProperty(land);
                } else if (type.equals("AgriculturalLand")) {
                    Person owner = findPersonById(Long.parseLong(parts[1]));
                    long regNo = Long.parseLong(parts[2]);
                    long zoneCode = Long.parseLong(parts[3]);
                    float size = Float.parseFloat(parts[4]);
                    RealEstate agriLand = new AgriculturalLand(owner, regNo, zoneCode, size);
                    owner.addProperty(agriLand);
                }
            }
        } catch (IOException e) {
            System.out.println("error loading data.");
        }
        for(Apartment apartment : apartments) {
            for (Building building : buildings) {
                if (building.getRegistrationNumber() == apartment.getRegistrationNumber()){
                    building.addApartment(apartment);
                    break;
                }
            }
        }
    }

    private static void saveToFile() {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter("output.txt"))) {
            for (Person person : persons) {
                bw.write("person: " + person.getName() + ", ID: " + person.getID());
                bw.newLine();
                for (RealEstate property : person.getProperties()) {
                    if (property instanceof House) {
                        House house = (House) property;
                        bw.write("  house:");
                        bw.newLine();
                        bw.write("    registration number: " + house.registrationNumber);
                        bw.newLine();
                        bw.write("    zone code: " + house.zoneCode);
                        bw.newLine();
                        bw.write("    size: " + house.size + " sq meters");
                        bw.newLine();
                        bw.write("    number of rooms: " + house.getNumOfRooms());
                        bw.newLine();
                        bw.write("    number of floors: " + house.getNumOfRooms());
                        bw.newLine();
                        bw.write("    construction year: " + new GregorianCalendar().get(Calendar.YEAR));
                        bw.newLine();
                        bw.write("    price: $" + house.getPrice());
                        bw.newLine();
                    } else if (property instanceof Building) {
                        Building building = (Building) property;
                        bw.write("  building:");
                        bw.newLine();
                        bw.write("    registration number: " + building.registrationNumber);
                        bw.newLine();
                        bw.write("    zone code: " + building.zoneCode);
                        bw.newLine();
                        bw.write("    price: $" + building.getPrice());
                        bw.newLine();
                        bw.write("    apartments:");
                        for (Apartment apartment : building.getApartments()) {
                            bw.newLine();
                            bw.write("      apartment:");
                            bw.newLine();
                            bw.write("        floor number: " + apartment.getFloorNumber());
                            bw.newLine();
                            bw.write("        size: " + apartment.size + " sq meters");
                            bw.newLine();
                            bw.write("        price: $" + apartment.getPrice());
                            bw.newLine();
                        }
                    } else if (property instanceof Land) {
                        Land land = (Land) property;
                        bw.write("  land:");
                        bw.newLine();
                        bw.write("    registration number: " + land.registrationNumber);
                        bw.newLine();
                        bw.write("    zone code: " + land.zoneCode);
                        bw.newLine();
                        bw.write("    size: " + land.size + " sq meters");
                        bw.newLine();
                        bw.write("    price: $" + land.getPrice());
                        bw.newLine();
                    } else if (property instanceof AgriculturalLand) {
                        AgriculturalLand agriLand = (AgriculturalLand) property;
                        bw.write("  agricultural land:");
                        bw.newLine();
                        bw.write("    registration number: " + agriLand.registrationNumber);
                        bw.newLine();
                        bw.write("    zone code: " + agriLand.zoneCode);
                        bw.newLine();
                        bw.write("    size: " + agriLand.size + " sq meters");
                        bw.newLine();
                        bw.write("    price: $" + agriLand.getPrice());
                        bw.newLine();
                    }
                }
                bw.newLine();
            }
        } catch (IOException e) {
            System.out.println("error saving data.");
        }
    }

}
