TRUNCATE TABLE Listings RESTART IDENTITY;

-- Insert fake listings
INSERT INTO Listings (user_id, title, description, price, img, name, mimetype) VALUES
(1, 'Cozy Apartment Downtown', 'A cozy 1-bedroom apartment in the heart of the city.', 1200.00, NULL, 'image1.png', 'image/png'),
(1, 'Spacious House with Garden', 'A beautiful 4-bedroom house with a large garden.', 2500.00, NULL, 'image2.png', 'image/png'),
(2, 'Modern Studio', 'A modern studio with a stunning view.', 900.00, NULL, 'image3.png', 'image/png'),
(2, 'Luxury Condo', 'A luxury condo with all amenities included.', 1800.00, NULL, 'image4.png', 'image/png'),
(3, 'Charming Cottage', 'A charming 2-bedroom cottage near the park.', 1500.00, NULL, 'image5.png', 'image/png'),
(3, 'Loft in Artistic Neighborhood', 'An artistic loft in a vibrant neighborhood.', 1600.00, NULL, 'image6.png', 'image/png'),
(4, 'Penthouse with Rooftop', 'A stunning penthouse with a private rooftop terrace.', 3000.00, NULL, 'image7.png', 'image/png'),
(5, 'Affordable Room for Rent', 'A clean room for rent in a friendly neighborhood.', 500.00, NULL, 'image8.png', 'image/png'),
(6, 'Family Home with Pool', 'A spacious family home with a large swimming pool.', 2200.00, NULL, 'image9.png', 'image/png'),
(7, 'Quiet Cabin in the Woods', 'A peaceful cabin for a weekend getaway.', 700.00, NULL, 'image10.png', 'image/png');

-- You can adjust the values for img, name, and mimetype based on your actual image handling setup.
