# Solution Approach

I refer to the task provided by your company as the *Gardener Route Planner*. To tackle this problem, I used an iterative development approach. Below is a breakdown of my iterations:

## Version 1: Minimum Viable Product

### Objective:

- Develop a basic version that allows users to input up to 10 destination addresses, automatically acquire the current location as the starting point, and compute and return the optimal round-trip route.

### Approach:

- **Core Functions**:
  - Users input up to 10 destination addresses via the frontend.
  - The backend uses a simple route planning algorithm to return a sequential order from the starting point to the destinations.
  - Display the computed route order (as a text list).
- **Implementation**:
  - **Frontend**: Built a simple interface using Bootstrap and jQuery, including input fields and a submit button.
  - **Backend**: Used the Django framework to handle user requests, receive the starting point and destination list, and return the shortest route (initially returned in input order).
  - **Interaction**: Users input addresses and submit via button; the backend returns and displays the route order.

### Technical Implementation:

- **Frontend**:
  - Used a `<textarea>` to allow input of multiple destination addresses.
  - Used `jQuery` to send an AJAX request to the backend to fetch the computed route.
- **Backend**:
  - Django receives the input and, for now, simply returns the route in input order.

## Version 2: Add Real-Time Location Feature

### Objective:

- Use the browser’s **HTML5 Geolocation API** to get the user’s current location.
- Use the current location as the starting point and send it to the backend.
- Display the acquired current location and the planned route.

### Implementation Steps:

1. **Frontend**: Use `navigator.geolocation.getCurrentPosition()` to get the device's current location.
2. **Backend**: The frontend already sends the starting location (latitude and longitude), so backend logic remains unchanged.
3. **Frontend Display**: Show the acquired location on the page and send it to the backend for route calculation.

### Changes:

Only frontend code needs modification to add real-time location functionality; backend code requires no major changes.

## Version 3: Integrate Amap API for Geocoding and Route Optimization

### Objective:

Integrate Amap (Gaode) API in the backend to implement geocoding (converting addresses to coordinates) and route optimization (calculating the best route).

### Implementation:

- The backend uses Amap's geocoding API to convert user-inputted addresses into latitude and longitude.
- Uses Amap’s routing service to calculate the optimal route from the starting point to the destinations and returns it to the frontend.
- The frontend draws the route based on data returned from the backend.

## Version 4: Add Map Display in Frontend

### Objective:

Use the **Amap JavaScript API** to display a map, mark locations, and draw the route. This allows users to visually see the starting point, destinations, and planned route in addition to the textual route instructions.

### Implementation:

- **Load Amap API**: Load Amap's JavaScript SDK using a `<script>` tag.
- **Create Map Instance**: Create a map container on the page.
- **Show Start and Destination Markers**: Add markers on the map.
- **Draw Optimized Route**: Use `AMap.Polyline` to draw the route returned from the backend.

## Version 5: Enhance Project Functionality

### Objective:

To make the project more robust, added input validation, error handling, and improved frontend styles.

### Implementation:

**Input Validation**:

- **Destination Input**: Check if the user’s address input is empty and limit input to a maximum of 10 destinations.
- **Clear Error Info**: Clear previous error messages when the user clicks "Plan Route" again.

**Error Handling**:

- **Location Failure**: Show an error if the browser fails to get the current location.
- **Backend Request Failure**: Display detailed error info if the backend request fails.
- **Invalid Input**: Show appropriate error messages if the address is invalid or exceeds limits.

**Style Cleanup**:

- Optimized page layout using `container` to restrict page width, making it cleaner.
- Adjusted button styles and map container height with CSS.

**Error Message Display**:

- Used Bootstrap’s `alert` component for user-friendly error messages.

## Version 6: Return Each Route Segment Individually

### Objective:

The previous functionality returned the entire optimized route in one go. This wasn’t very user-friendly on the frontend. Now, the system will **display the destination name as each segment is reached**, instead of showing the full route all at once.

### Implementation:

**Backend - Segmental Routing**:

In `views.py`, for each destination `dest`:

1. Convert it to coordinates;
2. Use the current `current` point as the starting point and request the route from `current → dest`;
3. Get the instructions and coordinate path for each segment;
4. Store the results in the list `steps[]`;
5. Update `current = dest` and move to the next destination.

**Frontend - Segmental Display**:

Upon receiving `routes[]`:

- Display "Arrived at: Destination"
- Show all instructions for that segment

## Version 7: Draw Full Optimized Route on Map

### Objective:

The backend returns each segment’s **coordinate path** (not just textual instructions). The frontend will draw each segment on the map using `Polyline`.

### Implementation:

**Backend**:

- Each route segment returns a list of coordinates: `[[lng, lat], [lng, lat], ...]`
- Merge all segments into one large path (array concatenation)

**Frontend**:

- Combine all segment paths `route.path` into one `fullPath`
- Use `AMap.Polyline` to draw it
- Use `map.setFitView()` to auto-zoom the map to fit the entire path

## My GitHub

This is the GitHub address of this project. If you are interested in the iteration process, you can click to access it

https://github.com/sunjl222/gardener_planner