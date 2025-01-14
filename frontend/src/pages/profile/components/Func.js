const getToken = () => {
    const token = localStorage.getItem("chronoJWTToken");
    if (!token) {
      throw new Error("Token is missing. Please log in.");
    }
    return token;
  };

  const fetchUser = async () => {
    try {
      const token = getToken();
      const response = await axios.get("http://localhost:8080/api/v1/user/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      user.value = response.data;
    } catch (error) {
      console.error("Error fetching user:", error);
    }
  };