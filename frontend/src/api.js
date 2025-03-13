const API_BASE_URL = "http://127.0.0.1:8000";

export const signUp = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/api/auth/signup/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  return response.json();
};

export const signIn = async (credentials) => {
  const response = await fetch(`${API_BASE_URL}/api/auth/signin`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  return response.json();
};

export const me = async (token) =>
{
  const responce = await fetch(`${API_BASE_URL}/me`,
  {
    method:"GET",
    headers:
    {
      "Content-Type":"application/json",
      "Authorization": `Bearer ${token}`,
    }
  })
  return await responce.json();
}

export const changeUser = async (token, userData) =>
{
  const responce = await fetch(`${API_BASE_URL}/me`,
  {
    method:"PATCH",
    headers:
    {
      "Content-Type":"application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify(userData)
})
  return await responce.json();
}

export const films = async () =>
{
  const responce = await fetch(`${API_BASE_URL}/films`,
  {
    method:"GET",
    headers:
    {
      "Content-Type":"application/json",
    }
  })
    return await responce.json();
}

export const filmId = async(id) =>
{
  const responce = await fetch(`${API_BASE_URL}/films/${id}`,
  {
    method:"GET",
    headers:
    {
      "Content-Type":"application/json",
    }
  })
  return await responce.json();
}

export const showtimes = async() =>
{
  const responce = await fetch(`${API_BASE_URL}/showtimes`,
    {
      method:"GET",
      headers:
      {
        "Content-Type":"application/json",
      }
    })
    return await responce.json();
}

export const showtime = async (id) =>
  {
    const responce = await fetch(`${API_BASE_URL}/showtimes/${id}`,
    {
      method:"GET",
      headers:
      {
        "Content-Type":"application/json",
      }
    })
    return await responce.json();
  }

  export const book = async (bookData, token) =>
    {
      const responce = await fetch(`${API_BASE_URL}/payments/book`,
      {
        method:"POST",
        headers:
        {
          "Content-Type":"application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(bookData)})
      return await responce.json();
    }

    export const pay = async (payData, token) =>
      {
        const responce = await fetch(`${API_BASE_URL}/payments/pay`,
        {
          method:"POST",
          headers:
          {
            "Content-Type":"application/json",
            "Authorization": `Bearer ${token}`,
          },
          body: JSON.stringify(payData)})
        return await responce.json();
      }

      export const history = async (token) =>
        {
          const responce = await fetch(`${API_BASE_URL}/payments/orders`,
          {
            method:"GET",
            headers:
            {
              "Content-Type":"application/json",
              "Authorization": `Bearer ${token}`,
            },})
          return await responce.json();
        }
