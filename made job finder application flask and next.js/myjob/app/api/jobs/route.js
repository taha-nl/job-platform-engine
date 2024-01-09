// app/api/route.js

export async function get() {
  try {
    // Fetch data from the Flask endpoint or perform other logic
    const response = await fetch('http://localhost:5000/');
    const data = await response.json();

    // Return the data
    return {
      props: {
        data,
      },
    };
  } catch (error) {
    console.error('Error fetching data:', error.message);
    return {
      props: {
        data: [],
      },
    };
  }
}
