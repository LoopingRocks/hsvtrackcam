import React from "react";
import {
  Container,
  Row,
  Col,
  Card,
  CardText,
  CardBody,
  CardTitle
} from "reactstrap";
import { PhotoshopPicker } from "react-color";

export default class Home extends React.Component {
  constructor(props) {
    super(props);

    this.changeColor = this.changeColor.bind(this);
    this.changeLowColor = this.changeLowColor.bind(this);
    this.changeHighColor = this.changeHighColor.bind(this);

    this.state = {};
  }

  changeLowColor(color) {
    this.changeColor(color, "low");
  }

  changeHighColor(color) {
    this.changeColor(color, "high");
  }

  changeColor(color, type) {
    const { hsv } = color;

    const value = {
      h: Math.floor((hsv.h * 255) / 360),
      s: Math.floor(hsv.s * 255),
      v: Math.floor(hsv.v * 255)
    };

    fetch(`/colors/${type}`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(value)
    });
  }

  render() {
    return (
      <div>
        <Card>
          <CardBody>
            <CardTitle>Select low and high color range</CardTitle>
            <CardText>
              On the left is the lower range color and on the right, the upper
              range color
            </CardText>
            <Container>
              <Row>
                <Col>
                  <img src="/stream.mjpg" width="640" height="480" alt="stream" />
                </Col>
              </Row>
              <Row>
                <Col>
                  <PhotoshopPicker onChangeComplete={this.changeLowColor} />
                </Col>
                <Col>
                  <PhotoshopPicker onChangeComplete={this.changeHighColor} />
                </Col>
              </Row>
            </Container>
          </CardBody>
        </Card>
      </div>
    );
  }
}
