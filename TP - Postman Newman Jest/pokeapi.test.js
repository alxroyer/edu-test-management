const axios = require("axios");

test("GET /pokemon/1 returns Bulbasaur", async () => {
    const response = await axios.get("https://pokeapi.co/api/v2/pokemon/1");
    expect(response.status).toBe(200);
    expect(response.data.name).toBe("bulbasaur");
    expect(response.data.types).toBeInstanceOf(Array);
});
