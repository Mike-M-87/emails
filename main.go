package main

import (
	"fmt"
	"log"
	"net/smtp"
	"os"
	"path/filepath"
	"strings"
	"time"
)

const (
	smtpServer   = "smtp.gmail.com"
	smtpPort     = 587
	senderEmail  = "your_email@gmail.com"
	senderPass   = "your_email_password"
	ticketsFolder = "path/to/your/tickets/folder"
	csvFilePath  = "path/to/your/csvfile.csv"
)

func main() {
	// Read emails from the CSV file
	emails, err := readEmails(csvFilePath)
	if err != nil {
		log.Fatal("Error reading emails:", err)
	}

	// Loop through each email
	for index, recipient := range emails {
		// Assuming tickets are named in a consistent way (e.g., Ticket 1.png, Ticket 2.png)
		ticketNumber := index + 1
		ticketFile := fmt.Sprintf("Ticket %d.png", ticketNumber)
		ticketPath := filepath.Join(ticketsFolder, ticketFile)

		// Create an email message
		msg := createEmail(recipient, ticketFile)

		// Attach the ticket file
		if err := attachTicket(msg, ticketPath); err != nil {
			log.Printf("Error attaching ticket for %s: %s. Skipping email.\n", recipient, err)
			continue
		}

		// Connect to the email server and send the email
		if err := sendEmail(msg, recipient); err != nil {
			log.Printf("Error sending email to %s: %s\n", recipient, err)
		}

		// Sleep for 100 milliseconds between sending emails
		time.Sleep(100 * time.Millisecond)
	}
}

func readEmails(filePath string) ([]string, error) {
	file, err := os.ReadFile(filePath)
	if err != nil {
		return nil, err
	}
	return strings.Split(string(file), "\n"), nil
}

func createEmail(recipient, ticketFile string) *Message {
	msg := NewMessage()
	msg.SetFrom(senderEmail)
	msg.AddTo(recipient)
	msg.SetSubject("Your Ticket")
	msg.SetBody(fmt.Sprintf("Dear recipient, please find your ticket (%s) attached.", ticketFile))
	return msg
}

func attachTicket(msg *Message, filePath string) error {
	data, err := os.ReadFile(filePath)
	if err != nil {
		return err
	}
	msg.Attach(MIMEApplication(data).SetType("png").SetHeader("Content-Disposition", fmt.Sprintf("attachment; filename=%s", filePath)))
	return nil
}

func sendEmail(msg *Message, recipient string) error {
	auth := smtp.PlainAuth("", senderEmail, senderPass, smtpServer)
	return smtp.SendMail(fmt.Sprintf("%s:%d", smtpServer, smtpPort), auth, senderEmail, []string{recipient}, msg.Bytes())
}
