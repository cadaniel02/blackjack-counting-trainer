import { observer } from 'mobx-react';
import React, { useEffect, useState } from 'react';

interface ApiResponse {
  message: string;
}

const SimpleApiComponent: React.FC = observer(function SimpleApiComponent()  {
  const [apiResponse, setApiResponse] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/simpleapi/');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data: ApiResponse = await response.json();
        setApiResponse(data);
      } catch (err) {
        if (err instanceof Error){
            setError(err.message)
        }
        else{
            setError("")
        }
      }
    };

    fetchData();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      {apiResponse ? <p>{apiResponse.message}</p> : <p>Loading...</p>}
    </div>
  );
});

export default SimpleApiComponent;