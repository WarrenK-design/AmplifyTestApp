import './App.css';
import { Tabs, Grid,Card,TabItem, withAuthenticator, Button, Text, Flex, Heading } from "@aws-amplify/ui-react";
import { useCallback, useEffect, useState } from 'react';
import { Amplify, API } from 'aws-amplify';
import awsconfig from './aws-exports';
import '@aws-amplify/ui-react/styles.css';

Amplify.configure(awsconfig);
API.configure(awsconfig);

const apiName = 'myExpressAPI'
const memberPath = '/members'
const projectGoalsPath = '/projectGoals'
const myInit = { // OPTIONAL
    headers: {}, // OPTIONAL
    response: true, // OPTIONAL (return the entire Axios response object instead of only response.data)
    queryStringParameters: {  // OPTIONAL
        name: 'param',
    },
};

function App() {
  const [members, setMembers] = useState([])
  const [projectGoals, setProjectGoals] = useState([])

  function getTeamMembers(e){
    e.preventDefault();
    API
      .get(apiName,memberPath, myInit)
      .then(response => {
        console.log(response)
        setMembers(response.data.message)
      })
      .catch(error => {
        console.log(error)
      })
  }

  function getProjectGoals(e){
    e.preventDefault();
    API
      .get(apiName,projectGoalsPath, myInit)
      .then(response => {
        console.log(response)
        setProjectGoals(response.data.message)
      })
      .catch(error => {
        console.log(error)
        console.log(error.response)
      })
  }

  return (
    <Grid
      columnGap="0.5rem"
      rowGap="0.5rem"
      templateColumns="1fr 1fr 1fr"
      templateRows="1fr 3fr 1fr"
    >
    <Card
      columnStart="1"
      columnEnd="-1"
    >
      <Heading level={1}>Future Great Stock App V3</Heading>
    </Card>
      <Card
      columnStart="1"
      columnEnd="-1">
      <Button onClick={getTeamMembers}>Get Team Members from /members API route</Button>
          <Flex>
            <p>{members}</p>
            </Flex>
          <Button onClick={getProjectGoals}>Get Project Goals from /projectGoals API Route</Button>
          <Flex>
            <p>{projectGoals}</p>
            </Flex>
      </Card>

    </Grid>
  );
}

export default App;