import pytest
from fastapi import status


async def register_candidate(client, jwt_token):
    """
    Register New candidates.
    """
    headers = {"Authorization": f"Bearer {jwt_token}"}
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "career_level": "Senior",
        "job_major": "Engineer",
        "years_of_experience": 5,
        "degree_type": "Bachelor",
        "skills": ["Python", "SQL"],
        "nationality": "Country",
        "city": "City",
        "salary": 80000.0,
        "gender": "Male"
    }

    response = await client.post("/candidate/create", headers=headers, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert "uuid" in response.json()
    assert response.json()["message"] == "Candidate Registered Successfully"

    return response.json()["uuid"]


class TestCandidates:

    @pytest.mark.anyio
    async def test_register_new_candidate(self, client, jwt_token):
        """
        Test case to register a new candidate and verify the success response.
        """
        candidate_id = await register_candidate(client, jwt_token)
        assert candidate_id

    @pytest.mark.anyio
    async def test_get_candidate_details(self, client, jwt_token):
        """
        Test case to retrieve details of a specific candidate.
        """
        candidate_id = await register_candidate(client, jwt_token)

        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = await client.get(f"/candidate/get/{candidate_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.anyio
    async def test_update_candidate_data(self, client, jwt_token):
        """
        Test case to update candidate data and verify the updated response.
        """
        headers = {"Authorization": f"Bearer {jwt_token}"}
        candidate_id = await register_candidate(client, jwt_token)

        payload = {
            "first_name": "Updated John",
            "last_name": "Updated Doe",
        }
        response = await client.put(f"/candidate/update/{candidate_id}", headers=headers, json=payload)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.anyio
    async def test_delete_candidate(self, client, jwt_token):
        """
        Test case to delete a candidate and verify the success response.
        """
        headers = {"Authorization": f"Bearer {jwt_token}"}
        candidate_id = await register_candidate(client, jwt_token)

        response = await client.delete(f"/candidate/delete/{candidate_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Record deleted successfully"

    @pytest.mark.anyio
    async def test_get_all_candidates_with_filters(self, client, jwt_token):
        """
        Test case to retrieve all candidates based on filters.
        """
        headers = {"Authorization": f"Bearer {jwt_token}"}
        await register_candidate(client, jwt_token)

        filters = {
            "first_name": "John",
        }
        response = await client.post("/candidate/all-candidates", headers=headers, json=filters)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.anyio
    async def test_generate_csv_report(self, client, jwt_token):
        """
        Test case to generate a CSV report of candidates.
        """
        headers = {"Authorization": f"Bearer {jwt_token}"}
        await register_candidate(client, jwt_token)

        response = await client.get("/candidate/generate-csv-report", headers=headers)
        assert response.status_code == status.HTTP_200_OK
