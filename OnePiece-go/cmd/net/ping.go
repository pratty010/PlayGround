/*
Copyright © 2023 NAME HERE <EMAIL ADDRESS>
*/
package net

import (
	"fmt"
	"log"
	"os/exec"

	"github.com/spf13/cobra"
)

var (
	ip    string
	count int
	ipv6  bool
)

func ping() {

	// fmt.Printf("%v %v %v", ip, count, ipv6)

	var args [2]string

	args[1] = fmt.Sprintf("-c %v", count)

	if ipv6 {
		args[0] = "-6"
	}

	// fmt.Printf(("ping %v %v %v"), args[0], args[1], ip)

	res, err := exec.Command("ping", args[0], args[1], ip).CombinedOutput()

	if err != nil {
		log.Fatalf("ping cmd failed for %s with %s\n", ip, err)
	}
	fmt.Printf("combined out:\n%s\n", string(res))
}

// pingCmd represents the ping command
var PingCmd = &cobra.Command{
	Use:   "ping",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,

	Run: func(cmd *cobra.Command, args []string) {
		ping()
	},
}

func init() {

	// Here you will define your flags and configuration settings.
	// pingCmd.Flags().BoolP()
	PingCmd.Flags().StringVarP(&ip, "ip", "i", "", "please input your IP")
	PingCmd.Flags().IntVarP(&count, "count", "c", 4, "please provide number of pings")
	PingCmd.Flags().BoolVarP(&ipv6, "ipv6", "6", false, "turn on IPv6 settings")

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// pingCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// pingCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")

	if err := PingCmd.MarkFlagRequired("ip"); err != nil {
		fmt.Printf("IP option missing.\nError > %s\n", err)
	}
	NetCmd.AddCommand(PingCmd)

}
